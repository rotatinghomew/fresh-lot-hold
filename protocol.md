# 标签与交接记录

`lineage` 的 lot 是实体标签，由 entity 标识所属门店或原料商。lot 标识全局唯一，不同商品的单位统一为净重克。source 行是供应商原箱，pack 行同时给出 input 标签及各自使用克数，已用原料与未用余料之和不能超过可用质量。`corrections` 引用原包装记录 id，提供完整替换的投入关系与申请和复核证据。修订不替换实体标签。

`transfers` 含 piece、lot、from、to、kind、occurred_at，piece 为可独立交接的配送件，店、配送和购买人都可作为 custody 端。待交接件的 order 关联同一顾客订单。customer 行另有 contact，contact 为空表示无可核实联系方式。客户通知以同一受影响配送件和顾客为业务对象。

`notices` 每个 notice 独立，revision 是通知的修订顺序。roots 指原料批号；shops 是当前覆盖门店，门店按成品处理点确定。effective_at 以前已送达的成品仍纳入追查和通知，但不能当成尚未出货拦回。放行按件和通知留存质量依据。时刻为带偏移的 ISO 8601。

交换样本为 UTF-8 NDJSON，每行独立。文件中的行顺序保留这组资料的原始提供顺序。
