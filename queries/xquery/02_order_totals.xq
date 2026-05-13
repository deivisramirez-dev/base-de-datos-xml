for $order in /commerce/orders/order
return
<order_total>
    <order_id>{data($order/@order_id)}</order_id>
    <total>{
        sum(
            for $item in $order/items/item
            return xs:decimal($item/unit_price) * xs:integer($item/quantity)
        )
    }</total>
</order_total>
