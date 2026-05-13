for $inv in /commerce/inventory/inventory_item
let $store := /commerce/stores/store[@store_id = $inv/store_id]
let $product := /commerce/products/product[@product_id = $inv/product_id]
return
<inventory_report>
    <store>{data($store/store_name)}</store>
    <product>{data($product/product_name)}</product>
    <available_units>{data($inv/product_inventory)}</available_units>
</inventory_report>
