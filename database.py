import os
import shelve
import shutil



class Database:
    def __init__(self, dbname: str, auto_save: bool = True) -> None:
        if dbname + '.dat' not in os.listdir('./db'):
            self.create_db(dbname)
        
        self.dbname: str = dbname
        self.auto_save: bool = auto_save
        self.data: shelve.Shelf = shelve.open(f'./db/{self.dbname}', writeback = self.auto_save)

    def put(self, table: str, data: dict) -> None:
        " Put data to db "
        if not self.db_is_open:
            raise DBException('Database already closed')
        
        general = self.data['general']
        data['id'] = general['current_id'] + 1
        self.data['general']['current_id'] = data['id']
        self.data[table][data['id']] = data

    def query(self, table: str, params: list[tuple[str]]) -> list[dict]:
        """ Query data from db
        table param can be any if you want to get from all tables
        """

        if table != 'any':
            table_instance = [value for nid, value in self.data[table].items()]
        else:
            table_instance = []
            for filename in os.listdir('./markup'):
                tablename, ext = filename.split('.')
                table_instance.extend([value for nid, value in self.data[tablename].items()])
        
        for param in params:
            table_instance = [value for value in table_instance if param[0] in value[param[1]]]
        return table_instance

    def get_page(self, table: str, notes_per_page: int, page: int) -> list:
        ' Get notes equal to "notes_per_page" with offest '
        if page > 0: page -= 1
        elif page < 0: page = 0
        notes_nids: list = list(self.data[table].keys())[page * notes_per_page:(page * notes_per_page) + notes_per_page]
        return [self.data[table][nid] for nid in notes_nids]

    def del_by_id(self, table: str, obj_id: int) -> None:
        ' Delete note in table by id '
        if obj_id not in self.data[table]:
            return
        del self.data[table][obj_id]

    def get_by_id(self, table: str, obj_id: int) -> dict:
        ' Return note by id '
        if obj_id not in self.data[table]:
            return {}
        return self.data[table][obj_id]

    def bind(self, first: int, second: int) -> None:
        ' Bind one obj_id to another obj_id '
        first_bindings = self.data['bindings'].get(first, [])
        first_bindings.append(second)
        self.data['bindings'][first] = first_bindings

        second_bindings = self.data['bindings'].get(second, [])
        second_bindings.append(first)
        self.data['bindings'][second] = second_bindings

    def unbind(self, first: int, second: int) -> None:
        ' Delete bind bitween two obj_id'
        first_bindings: list = self.data['bindings'].get(first, [])
        del first_bindings[first_bindings.index(second)]
        self.data['bindings'][first] = first_bindings

        second_bindings: list = self.data['bindings'].get(second, [])
        del second_bindings[second_bindings.index(first)]
        self.data['bindings'][second] = second_bindings

    def get_binds(self, obj_id: int) -> list:
        ' Get all binds from obj_id '
        return self.data['bindings'].get(obj_id, [])

    def create_db(self, dbname: str) -> None:
        ' Creating empty database'
        create_db(dbname, dbname)

    def open(self) -> None:
        ' Open db '
        self.data: shelve.Shelf = shelve.open(f'./db/{self.dbname}', writeback = self.auto_save)
    
    def rename(self, new_name: str) -> None:
        ' Save and close current db, rename and open again '
        self.close()
        rename_db(self.dbname, new_name)
        self.dbname = new_name
        self.open()

    def delete(self) -> None:
        ' Close current db and delete it '
        self.close()
        delete_db(self.dbname)

    def save(self) -> None:
        " Sync opened db "
        self.data.sync()

    def close(self, dry: bool = False) -> None:
        " Sync (or not if dry) and close opened db "
        if not dry:
            self.data.sync()
        self.data.close()
        self.data = None
    
    @property
    def db_is_open(self) -> bool:
        if self.data != None:
            return True
        return False


def delete_db(dbname: str) -> None:
    if not db_file_exist(dbname):
        raise DBException("DB files not exist")
    for file in os.listdir('./db/'):
        filename, ext = file.split('.')
        if filename == dbname:
            os.remove(f'./db/{file}')

def rename_db(old_name: str, new_name: str) -> None:
    if not db_file_exist(old_name):
        raise DBException("DB files not exist")
    for file in os.listdir('./db/'):
        filename, ext = file.split('.')
        if filename == old_name:
            shutil.move(f'./db/{old_name}.{ext}', f'./db/{new_name}.{ext}')

def create_db(dbname: str, db_user_name: str) -> None:
    ''' Creating empty database
        Table names are taken from the folder ./markup
    '''
    db = shelve.open(f'./db/{dbname}')
    for filename in os.listdir('./markup'):
        tablename, ext = filename.split('.')
        db[tablename] = {}
    
    db['bindings'] = {}
    db['chronolines'] = {}
    db['general'] = {'current_id': 0, 'db_user_name': db_user_name}
    db.sync()
    db.close()

def db_file_exist(dbname: str) -> bool:
    for file in os.listdir('./db/'):
        filename, ext = file.split('.')
        if filename == dbname:
            return True
    return False

def get_database_list() -> list[str]:
    ' Return list of created database filenames '
    database_list: list = []
    for file in os.listdir('./db'):
        filename, ext = file.split('.')
        if filename not in database_list:
            database_list.append(filename)
    return database_list

def nid_to_notes(nids: list[str]) -> list[dict]:
    pass


class DBException(Exception):
    pass
