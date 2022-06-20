insheet using basicData.csv, c n clear
drop if 統一編號 == . & 公司名稱 == "" & 英文名稱 == "" & 代表人姓名 == "" & 公司所在地 == "" & 英文地址 == "" & 電話 == "" & mail == "" & 資本總額元 == ""
drop if 統一編號 == . & 公司名稱 == "" & 英文名稱 == ""
export exc using 衛服部藥商藥廠資料查詢.xlsx, first(var) sheet("衛服部藥商藥廠資料查詢") sheetrep

