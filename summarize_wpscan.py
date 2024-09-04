import json
import csv
import sys

def summarize_wpscan(json_file, output_csv):
    try:
        with open(json_file, 'r') as file:
            data = json.load(file)
        
        with open(output_csv, mode='w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(['Category', 'Item', 'Details', 'Additional Info'])

            if "interesting_findings" in data:
                for finding in data['interesting_findings']:
                    writer.writerow([
                        'Interesting Finding',
                        finding.get('to_s', 'N/A'),
                        finding.get('url', 'N/A'),
                        ', '.join(finding.get('interesting_entries', []))
                    ])

            if "main_theme" in data:
                theme = data['main_theme']
                writer.writerow([
                    'Theme',
                    theme.get('style_name', 'N/A'),
                    theme.get('location', 'N/A'),
                    theme.get('version', {}).get('number', 'N/A')
                ])

            if "plugins" in data:
                for plugin_name, plugin_data in data['plugins'].items():
                    writer.writerow([
                        'Plugin',
                        plugin_data.get('slug', plugin_name),
                        plugin_data.get('location', 'N/A'),
                        plugin_data.get('version', {}).get('number', 'N/A')
                    ])

            if "vuln_api" in data and "error" in data["vuln_api"]:
                writer.writerow([
                    'Vulnerability API',
                    'Error',
                    data["vuln_api"]["error"],
                    'N/A'
                ])

        print(f"Le résumé des résultats de WPScan a été exporté vers {output_csv}")
    except Exception as e:
        print(f"Erreur lors de la création du résumé CSV : {e}")

def main():
    if len(sys.argv) != 3:
        print("Usage: python3 summarize_wpscan.py <wpscan_json_file> <output_csv_file>")
        sys.exit(1)

    json_file = sys.argv[1]
    output_csv = sys.argv[2]

    summarize_wpscan(json_file, output_csv)

if __name__ == "__main__":
    main()
