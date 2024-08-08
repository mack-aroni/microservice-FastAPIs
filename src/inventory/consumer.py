from main import redis, Product
import time

key = "order_completed"
group = "inventory-group"

# make redis group
try:
    redis.xgroup_create(key, group)
except:
    print("Group already exists")

# runloop
while True:
    try:
        results = redis.xreadgroup(group, key, {key: ">"}, None)
        # print(results)
        if results != []:
            # print(results)
            for result in results:
                obj = result[1][0][1]
                product = Product.get(obj["product_id"])
                print(product)
                product.quantity = product.quantity - int(obj["quantity"])
                product.save()

    except Exception as e:
        print(str(e))
    time.sleep(1)
