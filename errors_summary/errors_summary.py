# -*- coding: utf-8 -*-

import json
import argparse


def generate_error_report(error_file_path, errors_report_output_path):
    with open(errors_report_output_path, 'w') as errors_report_output_file:
        with open(error_file_path) as errors_input_file:
            for line, customer_row in enumerate(errors_input_file.readlines(), start=1):
                try:
                    customer_row_json = json.loads(customer_row)
                except:
                    errors_report_output_file.write(f'Line {line}: Input file is not a valid JSON')
                    errors_report_output_file.write('\n===\n')
                    continue
                try:
                    merchant_user_id = customer_row_json['customer']['merchant_user_id']
                except KeyError:
                    errors_report_output_file.write(f'Line {line}: customer.merchant_user_id is missing from record')
                    errors_report_output_file.write('\n===\n')
                    continue
                missing_keys = {'customer', 'addresses', 'payments', 'subscriptions'} - set(customer_row_json.keys())
                if missing_keys:
                    errors_report_output_file.write(
                        f'Customer {merchant_user_id} (line {line}): JSON record is missing the following key(s): {", ".join(missing_keys)}'
                    )
                    errors_report_output_file.write('\n===\n')
                    continue
                customer_errors = _extract_error_from_entity(customer_row_json['customer'])
                addresses_errors = _extract_errors_from_list_of_entities(customer_row_json['addresses'])
                payments_errors = _extract_errors_from_list_of_entities(customer_row_json['payments'])
                subscriptions_errors = _extract_errors_from_list_of_entities(customer_row_json['subscriptions'])
                errors_report = {"merchant_user_id": merchant_user_id, "errors": {}}
                if customer_errors:
                    errors_report["errors"].update({"customer": customer_errors})
                if addresses_errors:
                    errors_report["errors"].update({"addresses": addresses_errors})
                if payments_errors:
                    errors_report["errors"].update({"payments": payments_errors})
                if subscriptions_errors:
                    errors_report["errors"].update({"subscriptions": subscriptions_errors})
                json.dump(errors_report, errors_report_output_file, ensure_ascii=False, indent=2)
                errors_report_output_file.write('\n===\n')


def _extract_error_from_entity(og_entity):
    return og_entity.get('error') or {}


def _extract_errors_from_list_of_entities(og_entities):
    return [
        {og_entity.get('origin', {}).get('id', 'NO_ID'): _extract_error_from_entity(og_entity)}
        for og_entity in og_entities if _extract_error_from_entity(og_entity)
    ]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('errors_file_path', help='Path to the errors file we want to summarize')
    parser.add_argument('report_output_file_path', help='Path to the errors report to be generated')
    args = parser.parse_args()
    generate_error_report(args.errors_file_path, args.report_output_file_path)


if __name__ == '__main__':
    main()
