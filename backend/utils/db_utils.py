from sqlalchemy import inspect

def row_to_dict(row):
	"""
	row를 dict로 변환
	"""
	return {key: getattr(row, key) for key in inspect(row).attrs.keys()}
