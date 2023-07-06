import database



def run_db_tests():
    if db_test_1(): # Create, rename, delete
        print('Test 1 passed')
    if db_test_2(): # Create, put, get_by_id, put, get_page, bind, get_binds, unbind, close, delete
        print('Test 2 passed')
    if db_test_3(): # Query
        print('Test 3 passed')

def db_test_1():
    "Test create, rename, delete functions"
    db = database.Database('test')
    db.close()
    if not database.db_file_exist('test'):
        raise TestException('Test 1 failed [0]')

    database.rename_db('test', 'also_test')
    if not database.db_file_exist('also_test'):
        raise TestException('Test 1 failed [1]')
    if database.db_file_exist('test'):
        raise TestException('Test 1 failed [2]')

    database.delete_db('also_test')
    if database.db_file_exist('also_test'):
        raise TestException('Test 1 failed [3]')
    
    return True

def db_test_2():
    db = database.Database('test')
    db.data['test_table'] = {}

    db.put('test_table', {'title': 'test_note 1', 'int': '8900'})
    try:
        note = db.data['test_table'][1]
        if note['int'] != '8900':
            raise Exception()
    except Exception as err:
        print(f'Test 2 failed [0] {err}')
        return False
    db.put('test_table', {'titile': 'test_note 2', 'int': 2})
    

    page = db.get_page('test_table', 2, 1)
    if page != [{'title': 'test_note 1', 'int': '8900', 'id': 1}, {'titile': 'test_note 2', 'int': 2, 'id': 2}]:
        raise TestException('Test 2 failed [1]')
    db.bind(1, 2)
    if db.data['bindings'] != {1: [2], 2: [1]}:
        raise TestException('Test 2 failed [2]')
    if db.get_binds(1) != [2]: raise TestException('Test 2 failed [3]')
    if db.get_binds(0) != []: raise TestException('Test 2 failed [4]')
    db.unbind(1, 2)
    if db.get_binds(1) != []: raise TestException('Test 2 failed [5]')
    db.delete()
    return True

def db_test_3():
    db = database.Database('test')
    db.data['test_table'] = {}
    db.put('test_table', {'title': 'test note', 'int': '1'})
    db.put('test_table', {'title': 'another test note', 'int': '2'})
    if db.query('test_table', [('another test', 'title')]) != [{'title': 'another test note', 'int': '2', 'id': 2}]:
        raise TestException('Test 3 failed [0]')
    if db.query('test_table', [('another tests', 'title')]) != []:
        raise TestException('Test 3 failed [1]')
    #if db.query('test_table', ('1', 'id'))['id'] != 1:
    #    raise TestException('Test 3 failed [2]')
    db.delete()
    return True


class TestException(Exception):
    pass


if __name__ == '__main__':
    run_db_tests()
