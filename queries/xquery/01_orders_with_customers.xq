for $order in /commerce/orders/order
let $customer := /commerce/customers/customer[@customer_id = $order/customer_id]
let $store := /commerce/stores/store[@store_id = $order/store_id]
return
<order_summary>
    <order_id>{data($order/@order_id)}</order_id>
    <customer>{data($customer/full_name)}</customer>
    <store>{data($store/store_name)}</store>
    <status>{data($order/order_status)}</status>
</order_summary>
