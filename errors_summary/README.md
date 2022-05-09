### Requirements
* Python 3.x


### About

The purpose of this script is to try and help you understand more quickly what went wrong
with a particular customer using our migration tools.

### Usage

```sh
$ python errors_summary.py migration_error_file.json error_summary_output_file.json
```

* The first argument is meant to be the path, including filename, to the Ordergroove migration error files
* The second argument is meant to be the path, including filename, to summary file

#### Sample output
If you were to open `error_summary_output_file.json` you might see something like

```
{
  "merchant_user_id": "5057992261799",
  "errors": {
    "addresses": [
      {
        "64602275": {
          "address_type": [
            "Unsupported value. Expecting \"shipping_address\" or \"billing_address\""
          ]
        }
      }
    ],
    "payments": [
      {
        "3583327": {
          "origin": [
            "Unsupported payment_processor type specified",
            "unknown origin.payment_processor.type; expected stripe, paypal or authorize"
          ]
        }
      }
    ],
    "subscriptions": [
      {
        "136977932": {
          "every_period": [
            "Expecting day, week, month"
          ],
          "quantity": [
            "Expecting an integer"
          ],
          "product": [
            "Product does not exist"
          ],
          "origin": [
            "Shipping address does not exist"
          ]
        }
      }
    ]
  }
}
===
```

The intent of this to allow you to make remediating errors easier:
* Open the migration file
* In this instance, search for "5057992261799" - which will take you directly to the row of the customer
* You can then search for "136977932" - which corresponds to the specific subscription within that row
* Finally, find the field or fields referenced by the error summary above and modify accordingly
