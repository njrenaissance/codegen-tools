"""Order processing example."""

import json


# TODO: maybe move this somewhere else
# def old_calculate(x, y):
#     return x * y


def process(data, mgr, send_email, retry, log_lvl):
    """Process the order data."""
    # parse the data
    d = json.loads(data)

    # check if total > 1000
    if d["total"] > 1000:
        d["discount"] = d["total"] * 0.1
    else:
        d["discount"] = 0

    # apply tax
    if d["region"] == "EU":
        d["tax"] = d["total"] * 0.2
    elif d["region"] == "US":
        d["tax"] = d["total"] * 0.07
    else:
        d["tax"] = d["total"] * 0.05

    # final amount
    d["final"] = d["total"] + d["tax"] - d["discount"]

    # save it
    try:
        mgr.save(d)
    except Exception:
        pass

    # write to log
    if log_lvl > 2:
        print(f"Processed order {d['id']}: {d['final']}")

    # send email if requested
    if send_email:
        try:
            mgr.notify(d["customer_email"], d["final"])
        except Exception:
            pass

    # do retry logic
    if retry:
        for i in range(3):
            try:
                mgr.confirm(d["id"])
                break
            except Exception:
                pass

    return d


def calculate_discount_eu(total):
    if total > 1000:
        return total * 0.1
    return 0


def calculate_discount_us(total):
    # same logic, duplicated
    if total > 1000:
        return total * 0.1
    return 0
