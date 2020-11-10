# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import sqlite3

class LinkextractorPipeline:
	def process_item(self, item, spider):
		return item


class ItemList:
	def process_item(self, item, spider):
		
		item['name'] = item.get('name').strip()
		item['raiting'] = item.get('raiting').strip()
		item['type'] = item.get('type').strip()
		item['price'] = item.get('price').strip()
		item['availability'] = item.get('availability').strip()
		item['description'] = item.get('description').strip()
		print()
		return item

class ItemRaiting:
	def process_item(self, item, spider):

		textToNumber = {'One': 1,
						'Two': 2,
						'Three': 3,
						'Four': 4,
						'Five': 5}
		
		item['raiting'] = textToNumber[item['raiting']]

		return item

class ItemAvailability:
	def process_item(self, item, spider):
		item['availability'] = item['availability'][10:-11]
		return item

class ItemPrice:
	def process_item(self, item, spider):
		item['price'] = item['price'][1:]
		return item

class extract:
	conn = sqlite3.connect('books.db')
	cursor = conn.cursor()

	def open_spider(self, spider):
		self.cursor.execute('''delete from books''')
		self.conn.commit()
	def process_item(self, item, spider):

		self.cursor.execute('''create table if not exists "books" (
			name text,
			raiting number,
			type text,
			price number,
			availability number,
			description varchar(255)
			) ''')

		name = item['name']
		raiting = int(item['raiting'])
		type = item['type']
		price = float(item['price'])
		availability = int(item['availability'])
		description = item['description']

		self.cursor.execute(f"""insert into books (name, raiting, type, price, availability, description) values (?, ?, ?, ?, ?, ?)""", (name, raiting, type, price, availability, description))

		return item

	def close_spider(self, spider):
		self.conn.commit()
		self.cursor.close()
		self.conn.close()
