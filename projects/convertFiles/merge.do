cd D:/Documents/python/projects/convertFiles/csvChiToEng/csv

foreach w in 生醫上市櫃營收Top20 生醫上市營收Top20 生醫上櫃營收Top20 生醫興櫃營收Top20 {
	insheet using `w'_eng.csv, c n clear
	save `w'_eng, replace
	insheet using `w'.csv, clear
	merge 1:m 公司名稱 using `w'_eng, force
	drop if _merge == 2
	drop _merge
	sort *排名
	ren v5 公司名稱英文
	order *排名 公司名稱 公司名稱英文
	outsheet using `w'_merge.csv, c n replace
	export exc using 2022Q1eng.xlsx, sh("`w'") first(var) sheetrep
}
