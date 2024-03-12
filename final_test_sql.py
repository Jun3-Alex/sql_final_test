'''
1.Создайте функцию, которая принимает кол-во сек и формат их в кол-во дней часов.
Пример: 123456 ->'1 days 10 hours 17 minutes 36 seconds '


2.Выведите только числа, делящиеся на 15 или 33 в промежутке от 1 до 1000.
Пример: 15,30,33,45...
'''

import configparser
import mysql.connector

config = configparser.ConfigParser()

config.read('config.ini')

connection = mysql.connector.connect(
    host=config['mysql']['host'],
    user=config['mysql']['user'],
    passwd=config['mysql']['passwd'],
    database=config['mysql']['database']
)

cursor = connection.cursor()

cursor.execute("DROP FUNCTION IF EXISTS seconds_to_dhms")

cursor.execute(
    '''
        CREATE FUNCTION seconds_to_dhms(seconds INT)
        RETURNS VARCHAR(50) READS SQL DATA
        BEGIN
            DECLARE days INT;
            DECLARE hours INT;
            DECLARE minutes INT;
            DECLARE remaining_seconds INT;
            SET days = seconds DIV (24 * 60 * 60);
            SET hours = (seconds MOD (24 * 60 * 60)) DIV (60 * 60);
            SET minutes = (seconds MOD (60 * 60)) DIV 60;
            SET remaining_seconds = seconds MOD 60;
            RETURN CONCAT(days, ' days ', hours, ' hours ', minutes, ' minutes ', 
                        remaining_seconds, ' seconds');
        END;

    '''
)

cursor.execute("SELECT seconds_to_dhms(12453);")

results = cursor.fetchall()

for row in results:
    print(row)

cursor.execute("DROP FUNCTION IF EXISTS find_numbers")

cursor.execute(
    '''
        CREATE FUNCTION find_numbers()
        RETURNS TEXT
        READS SQL DATA
        BEGIN
            DECLARE i INT DEFAULT 1;
            DECLARE result TEXT DEFAULT '';

            WHILE i <= 1000 DO
                IF i % 15 = 0 OR i % 33 = 0 THEN
                    SET result = CONCAT_WS(',', result, i);
                END IF;
                SET i = i + 1;
            END WHILE;

            RETURN TRIM(LEADING ',' FROM result);
        END;

    '''
)

cursor.execute("SELECT find_numbers();")

results = cursor.fetchall()

for row in results:
    print(row)

cursor.close()
connection.close()
