import sqlite3
import random
from datetime import datetime

class ProductDB:
    def __init__(self, db_name='MyProduct.db'):
        """데이터베이스 연결 및 테이블 생성"""
        self.db_name = db_name
        self.conn = None
        self.cursor = None
        self.connect()
        self.create_table()
    
    def connect(self):
        """데이터베이스 연결"""
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()
            print(f"✓ {self.db_name} 데이터베이스 연결 성공")
        except sqlite3.Error as e:
            print(f"✗ 데이터베이스 연결 실패: {e}")
    
    def create_table(self):
        """Products 테이블 생성"""
        try:
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS Products (
                    productID INTEGER PRIMARY KEY AUTOINCREMENT,
                    productName TEXT NOT NULL,
                    productPrice INTEGER NOT NULL
                )
            ''')
            self.conn.commit()
            print("✓ Products 테이블 준비 완료")
        except sqlite3.Error as e:
            print(f"✗ 테이블 생성 실패: {e}")
    
    def insert(self, product_name, product_price):
        """단일 제품 데이터 삽입"""
        try:
            self.cursor.execute('''
                INSERT INTO Products (productName, productPrice)
                VALUES (?, ?)
            ''', (product_name, product_price))
            self.conn.commit()
            return self.cursor.lastrowid
        except sqlite3.Error as e:
            print(f"✗ 삽입 실패: {e}")
            return None
    
    def insert_many(self, data_list):
        """대량 제품 데이터 삽입"""
        try:
            self.cursor.executemany('''
                INSERT INTO Products (productName, productPrice)
                VALUES (?, ?)
            ''', data_list)
            self.conn.commit()
            print(f"✓ {len(data_list)}개 데이터 삽입 완료")
            return True
        except sqlite3.Error as e:
            print(f"✗ 대량 삽입 실패: {e}")
            return False
    
    def select_all(self):
        """모든 제품 조회"""
        try:
            self.cursor.execute('SELECT * FROM Products')
            rows = self.cursor.fetchall()
            return rows
        except sqlite3.Error as e:
            print(f"✗ 조회 실패: {e}")
            return []
    
    def select_by_id(self, product_id):
        """ID로 제품 조회"""
        try:
            self.cursor.execute('''
                SELECT * FROM Products WHERE productID = ?
            ''', (product_id,))
            row = self.cursor.fetchone()
            return row
        except sqlite3.Error as e:
            print(f"✗ 조회 실패: {e}")
            return None
    
    def select_by_name(self, product_name):
        """제품명으로 검색"""
        try:
            self.cursor.execute('''
                SELECT * FROM Products WHERE productName LIKE ?
            ''', (f'%{product_name}%',))
            rows = self.cursor.fetchall()
            return rows
        except sqlite3.Error as e:
            print(f"✗ 검색 실패: {e}")
            return []
    
    def select_by_price_range(self, min_price, max_price):
        """가격 범위로 조회"""
        try:
            self.cursor.execute('''
                SELECT * FROM Products 
                WHERE productPrice BETWEEN ? AND ?
            ''', (min_price, max_price))
            rows = self.cursor.fetchall()
            return rows
        except sqlite3.Error as e:
            print(f"✗ 조회 실패: {e}")
            return []
    
    def update(self, product_id, product_name=None, product_price=None):
        """제품 정보 업데이트"""
        try:
            if product_name is not None and product_price is not None:
                self.cursor.execute('''
                    UPDATE Products 
                    SET productName = ?, productPrice = ?
                    WHERE productID = ?
                ''', (product_name, product_price, product_id))
            elif product_name is not None:
                self.cursor.execute('''
                    UPDATE Products 
                    SET productName = ?
                    WHERE productID = ?
                ''', (product_name, product_id))
            elif product_price is not None:
                self.cursor.execute('''
                    UPDATE Products 
                    SET productPrice = ?
                    WHERE productID = ?
                ''', (product_price, product_id))
            
            self.conn.commit()
            if self.cursor.rowcount > 0:
                print(f"✓ ID {product_id} 제품 업데이트 완료")
                return True
            else:
                print(f"✗ ID {product_id}인 제품을 찾을 수 없습니다")
                return False
        except sqlite3.Error as e:
            print(f"✗ 업데이트 실패: {e}")
            return False
    
    def delete(self, product_id):
        """제품 삭제"""
        try:
            self.cursor.execute('''
                DELETE FROM Products WHERE productID = ?
            ''', (product_id,))
            self.conn.commit()
            if self.cursor.rowcount > 0:
                print(f"✓ ID {product_id} 제품 삭제 완료")
                return True
            else:
                print(f"✗ ID {product_id}인 제품을 찾을 수 없습니다")
                return False
        except sqlite3.Error as e:
            print(f"✗ 삭제 실패: {e}")
            return False
    
    def delete_all(self):
        """모든 제품 삭제"""
        try:
            self.cursor.execute('DELETE FROM Products')
            self.conn.commit()
            print(f"✓ 모든 데이터 삭제 완료 ({self.cursor.rowcount}개)")
            return True
        except sqlite3.Error as e:
            print(f"✗ 삭제 실패: {e}")
            return False
    
    def count_products(self):
        """제품 총 개수 조회"""
        try:
            self.cursor.execute('SELECT COUNT(*) FROM Products')
            count = self.cursor.fetchone()[0]
            return count
        except sqlite3.Error as e:
            print(f"✗ 개수 조회 실패: {e}")
            return 0
    
    def get_statistics(self):
        """가격 통계 조회"""
        try:
            self.cursor.execute('''
                SELECT 
                    COUNT(*) as total_count,
                    AVG(productPrice) as avg_price,
                    MIN(productPrice) as min_price,
                    MAX(productPrice) as max_price
                FROM Products
            ''')
            stats = self.cursor.fetchone()
            return {
                'total': stats[0],
                'average': round(stats[1], 2) if stats[1] else 0,
                'minimum': stats[2],
                'maximum': stats[3]
            }
        except sqlite3.Error as e:
            print(f"✗ 통계 조회 실패: {e}")
            return None
    
    def close(self):
        """데이터베이스 연결 종료"""
        if self.conn:
            self.conn.close()
            print("✓ 데이터베이스 연결 종료")


def generate_sample_data(count=100000):
    """샘플 데이터 생성"""
    product_models = [
        'Laptop', 'Desktop', 'Monitor', 'Keyboard', 'Mouse',
        'Printer', 'Scanner', 'Router', 'Modem', 'Camera',
        'Headphones', 'Speaker', 'Microphone', 'Webcam', 'USB Hub',
        'SSD', 'HDD', 'RAM', 'Motherboard', 'Power Supply'
    ]
    
    brands = ['Samsung', 'LG', 'HP', 'Dell', 'ASUS', 'Sony', 'Nikon', 'Canon', 'Apple', 'Microsoft']
    
    data = []
    for i in range(count):
        product_name = f"{random.choice(brands)} {random.choice(product_models)} Model-{i+1:06d}"
        product_price = random.randint(10000, 5000000)
        data.append((product_name, product_price))
    
    return data


if __name__ == '__main__':
    # 1. 데이터베이스 초기화
    print("=" * 60)
    print("SQLite 전자제품 데이터베이스 시스템")
    print("=" * 60)
    
    db = ProductDB('MyProduct.db')
    
    # 2. 기존 데이터 확인
    existing_count = db.count_products()
    print(f"\n현재 데이터 개수: {existing_count}개")
    
    # 3. 데이터가 없으면 샘플 데이터 생성 및 삽입
    if existing_count == 0:
        print("\n샘플 데이터 생성 중... (10만개)")
        print(f"⏳ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} 시작")
        
        sample_data = generate_sample_data(100000)
        db.insert_many(sample_data)
        
        print(f"✓ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} 완료")
    
    # 4. 데이터 통계
    print("\n" + "=" * 60)
    print("데이터베이스 통계")
    print("=" * 60)
    stats = db.get_statistics()
    if stats:
        print(f"총 개수        : {stats['total']:,}개")
        print(f"평균 가격      : ₩{stats['average']:,.0f}")
        print(f"최저 가격      : ₩{stats['minimum']:,.0f}")
        print(f"최고 가격      : ₩{stats['maximum']:,.0f}")
    
    # 5. 샘플 쿼리 실행
    print("\n" + "=" * 60)
    print("샘플 쿼리 실행")
    print("=" * 60)
    
    # 5-1. 처음 5개 상품 조회
    print("\n[1] 처음 5개 상품 조회:")
    all_products = db.select_all()[:5]
    for product in all_products:
        print(f"  ID: {product[0]:6d} | {product[1]:50s} | ₩{product[2]:>10,}")
    
    # 5-2. ID로 조회
    print("\n[2] ID 5번 상품 조회:")
    product = db.select_by_id(5)
    if product:
        print(f"  ID: {product[0]} | {product[1]} | ₩{product[2]:,}")
    
    # 5-3. 특정 가격대 조회
    print("\n[3] 100만원 ~ 150만원 가격대 상품 (최대 5개):")
    products = db.select_by_price_range(1000000, 1500000)[:5]
    for product in products:
        print(f"  ID: {product[0]:6d} | {product[1]:50s} | ₩{product[2]:>10,}")
    
    # 5-4. 업데이트 샘플
    print("\n[4] ID 1번 상품 업데이트 (가격: 2,000,000원):")
    db.update(1, product_price=2000000)
    product = db.select_by_id(1)
    if product:
        print(f"  ID: {product[0]} | {product[1]} | ₩{product[2]:,}")
    
    # 6. 사용 가능한 메서드 안내
    print("\n" + "=" * 60)
    print("사용 가능한 메서드")
    print("=" * 60)
    print("""
    📝 INSERT 관련
    - insert(product_name, product_price)      : 단일 상품 추가
    - insert_many(data_list)                   : 대량 상품 추가
    
    📖 SELECT 관련
    - select_all()                             : 모든 상품 조회
    - select_by_id(product_id)                 : ID로 조회
    - select_by_name(product_name)             : 이름으로 검색
    - select_by_price_range(min, max)          : 가격 범위로 조회
    - count_products()                         : 총 개수 조회
    - get_statistics()                         : 통계 정보 조회
    
    ✏️  UPDATE 관련
    - update(product_id, name, price)          : 상품 정보 수정
    
    🗑️  DELETE 관련
    - delete(product_id)                       : 특정 상품 삭제
    - delete_all()                             : 모든 상품 삭제
    
    🔌 기타
    - close()                                  : 데이터베이스 연결 종료
    """)
    
    # 7. 연결 종료
    db.close()