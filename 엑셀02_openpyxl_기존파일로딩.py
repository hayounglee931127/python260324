import openpyxl as op 

#파일이 있는 상태에서 수행
wb = op.load_workbook("test.xlsx") #메서드로 인스턴스 생성

#새로운 시트 추가 
ws = wb.create_sheet("직원명부")

wb.save("test2.xlsx")

