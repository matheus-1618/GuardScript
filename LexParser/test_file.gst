str:file_name = "ryuk.exe"
rule:rules_ryuk {
 str:a = ".php?",
 str:b = "uid=",
 str:c = "&uname=",
}
if match(file_name, rules_ryuk){
  show("Arquivo suspeito")
} else{
  show("Arquivo normal")
}