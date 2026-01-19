"""
Data Exporter
Export scraped product data to various formats (JSON, CSV, Excel).
"""

import json
import csv
import os
from typing import List, Dict
from datetime import datetime
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO)


class DataExporter:
    """Export scraped data to various file formats."""

    def __init__(self, output_dir: str = "output"):
        """
        Initialize the data exporter.

        Args:
            output_dir: Directory to save exported files
        """
        self.output_dir = output_dir
        self.logger = logging.getLogger(__name__)
        self._ensure_output_dir()

    def _ensure_output_dir(self):
        """Create output directory if it doesn't exist."""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
            self.logger.info(f"Created output directory: {self.output_dir}")

    def _generate_filename(self, format: str, prefix: str = "products") -> str:
        """
        Generate timestamped filename.

        Args:
            format: File format extension
            prefix: Filename prefix

        Returns:
            Full file path
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{prefix}_{timestamp}.{format}"
        return os.path.join(self.output_dir, filename)

    def export_json(self, data: List[Dict], filename: str = None, pretty: bool = True) -> str:
        """
        Export data to JSON format.

        Args:
            data: List of product dictionaries
            filename: Custom filename (optional)
            pretty: Whether to format JSON with indentation

        Returns:
            Path to exported file
        """
        if filename is None:
            filename = self._generate_filename('json')
        elif not filename.startswith(self.output_dir):
            filename = os.path.join(self.output_dir, filename)

        try:
            with open(filename, 'w', encoding='utf-8') as f:
                if pretty:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                else:
                    json.dump(data, f, ensure_ascii=False)

            self.logger.info(f"Exported {len(data)} products to JSON: {filename}")
            return filename
        except Exception as e:
            self.logger.error(f"Failed to export JSON: {e}")
            raise

    def export_csv(self, data: List[Dict], filename: str = None, flatten: bool = True) -> str:
        """
        Export data to CSV format.

        Args:
            data: List of product dictionaries
            filename: Custom filename (optional)
            flatten: Whether to flatten nested structures

        Returns:
            Path to exported file
        """
        if not data:
            self.logger.warning("No data to export")
            return ""

        if filename is None:
            filename = self._generate_filename('csv')
        elif not filename.startswith(self.output_dir):
            filename = os.path.join(self.output_dir, filename)

        try:
            if flatten:
                data = [self._flatten_dict(item) for item in data]

            fieldnames = self._get_all_keys(data)

            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(data)

            self.logger.info(f"Exported {len(data)} products to CSV: {filename}")
            return filename
        except Exception as e:
            self.logger.error(f"Failed to export CSV: {e}")
            raise

    def export_excel(self, data: List[Dict], filename: str = None, flatten: bool = True) -> str:
        """
        Export data to Excel format.

        Args:
            data: List of product dictionaries
            filename: Custom filename (optional)
            flatten: Whether to flatten nested structures

        Returns:
            Path to exported file
        """
        if not data:
            self.logger.warning("No data to export")
            return ""

        if filename is None:
            filename = self._generate_filename('xlsx')
        elif not filename.startswith(self.output_dir):
            filename = os.path.join(self.output_dir, filename)

        try:
            if flatten:
                data = [self._flatten_dict(item) for item in data]

            df = pd.DataFrame(data)

            with pd.ExcelWriter(filename, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name='Products')

                worksheet = writer.sheets['Products']
                for idx, col in enumerate(df.columns):
                    max_length = max(
                        df[col].astype(str).apply(len).max(),
                        len(str(col))
                    )
                    worksheet.column_dimensions[chr(65 + idx)].width = min(max_length + 2, 50)

            self.logger.info(f"Exported {len(data)} products to Excel: {filename}")
            return filename
        except Exception as e:
            self.logger.error(f"Failed to export Excel: {e}")
            raise

    def export_all(self, data: List[Dict], prefix: str = "products") -> Dict[str, str]:
        """
        Export data to all supported formats.

        Args:
            data: List of product dictionaries
            prefix: Filename prefix for all files

        Returns:
            Dictionary mapping format to file path
        """
        results = {}

        try:
            results['json'] = self.export_json(data, f"{prefix}.json")
        except Exception as e:
            self.logger.error(f"JSON export failed: {e}")

        try:
            results['csv'] = self.export_csv(data, f"{prefix}.csv")
        except Exception as e:
            self.logger.error(f"CSV export failed: {e}")

        try:
            results['excel'] = self.export_excel(data, f"{prefix}.xlsx")
        except Exception as e:
            self.logger.error(f"Excel export failed: {e}")

        return results

    def _flatten_dict(self, d: Dict, parent_key: str = '', sep: str = '_') -> Dict:
        """
        Flatten nested dictionary.

        Args:
            d: Dictionary to flatten
            parent_key: Parent key for recursion
            sep: Separator for nested keys

        Returns:
            Flattened dictionary
        """
        items = []

        for k, v in d.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k

            if isinstance(v, dict):
                items.extend(self._flatten_dict(v, new_key, sep=sep).items())
            elif isinstance(v, list):
                if v and isinstance(v[0], dict):
                    items.append((new_key, json.dumps(v)))
                else:
                    items.append((new_key, ', '.join(map(str, v))))
            else:
                items.append((new_key, v))

        return dict(items)

    def _get_all_keys(self, data: List[Dict]) -> List[str]:
        """
        Get all unique keys from a list of dictionaries.

        Args:
            data: List of dictionaries

        Returns:
            List of all unique keys
        """
        keys = set()
        for item in data:
            keys.update(item.keys())
        return sorted(list(keys))
