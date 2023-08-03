import os
import shelve
import shutil
import pickle


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

    def del_by_nid(self, table: str, nid: int) -> None:
        ' Delete note in table by nid '
        if nid not in self.data[table]:
            return
        del self.data[table][nid]

    def get_by_nid(self, table: str, nid: int) -> dict:
        ' Return note by nid '
        if nid not in self.data[table]:
            return {}
        return self.data[table][nid]

    def bind(self, first: int, second: int) -> None:
        ' Bind one nid to another nid '
        first_bindings = self.data['bindings'].get(first, [])
        first_bindings.append(second)
        self.data['bindings'][first] = first_bindings

        second_bindings = self.data['bindings'].get(second, [])
        second_bindings.append(first)
        self.data['bindings'][second] = second_bindings

    def unbind(self, first: int, second: int) -> None:
        ' Delete bind bitween two nid'
        first_bindings: list = self.data['bindings'].get(first, [])
        del first_bindings[first_bindings.index(second)]
        self.data['bindings'][first] = first_bindings

        second_bindings: list = self.data['bindings'].get(second, [])
        del second_bindings[second_bindings.index(first)]
        self.data['bindings'][second] = second_bindings

    def get_binds(self, nid: int) -> list:
        ' Get all binds from nid '
        return self.data['bindings'].get(nid, [])

    def create_db(self, dbname: str) -> None:
        ' Creating empty database'
        create_db(dbname, dbname)

    def open(self) -> None:
        ' Open db '
        self.data: shelve.Shelf = shelve.open(f'./db/{self.dbname}', writeback = self.auto_save)
    
    def rename(self, new_name: str, name_type: str = 'udbname') -> None:
        ' Save and close current db, rename and open again '
        self.close()
        rename_db(self.dbname, new_name, name_type)
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

def rename_db(dbfilename: str, new_name: str, name_type: str = 'udbname') -> None:
    ''' Rename database depending "name_type"
        name_type: str = 'udbname', 'dbname'
    '''
    if not db_file_exist(dbfilename):
        raise DBException(f'DB files not exist [{dbfilename}]')

    if name_type == 'udbname':
        with shelve.open(f'./db/{dbfilename}') as db:
            general = db['general']
            general['udbname'] = new_name
            db['general'] = general
    if name_type == 'dbname':
        with shelve.open(f'./db/{dbfilename}') as db:
            general = db['general']
            general['dbname'] = new_name
            db['general'] = general
        for file in os.listdir('./db/'):
            filename, ext = file.split('.')
            if filename == dbfilename:
                shutil.move(f'./db/{dbfilename}.{ext}', f'./db/{new_name}.{ext}')

def create_db(dbname: str, udbname: str) -> None:
    ''' Creating empty database
        Table names are taken from the folder ./markup
    '''
    if udbname is None or udbname == '':
        udbname = dbname
    db = shelve.open(f'./db/{dbname}')
    #for filename in os.listdir('./markup'):
    #    tablename, ext = filename.split('.')
    #    db[tablename] = {}
    
    db['bindings'] = {}
    db['chronolines'] = {}
    db['general'] = {'current_id': 0, 'udbname': udbname, 'dbname': dbname}
    db['general']['tables'] = {}
    db.sync()
    db.close()

def duplicate_db(dbfilename: str) -> None:
    for file in os.listdir('./db'):
        filename, ext = file.split('.')
        if filename == dbfilename:
            shutil.copy(f'./db/{file}', f'./db/{filename}_copy.{ext}')
    with shelve.open(f'./db/{dbfilename}_copy') as db:
        general = db['general']
        general['udbname'] = general['udbname'] + ' Копия'
        db['general'] = general

def export_db(dbname: str, path: str, filename: str) -> None:
    package = {}
    with shelve.open(f'./db/{dbname}') as db:
        for section in db:
            package[section] = db[section]
    with open(os.path.join(path, f'{filename}.wad'), 'wb') as file:
        pickle.dump(package, file)

def import_db(path: str) -> None:
    with open(path, 'rb') as file:
        package = pickle.load(file)
    with shelve.open(f'./db/{package["general"]["dbname"]}') as db:
        for section in package:
            db[section] = package[section]

def get_db_names(name_type: str) -> list[str] or dict[str:str]:
    ' Return list of dbnames, udbnames or both '
    dbnames: list  = list(set([name.split('.')[0].strip() for name in os.listdir('./db')]))
    udbnames: list = []

    if name_type == 'dbname':
        return dbnames
    if name_type == 'udbname' or name_type == 'both':
        for dbname in dbnames:
            with shelve.open(f'./db/{dbname}') as db:
                udbnames.append(db['general']['udbname'])
        if name_type == 'udbname':
            return udbnames
    if name_type == 'both':
        return {dbname: udbnames[index] for index, dbname in enumerate(dbnames)}

def name_convert(name: str, convert_type: str) -> str:
    ' Convert udbname or dbname to another '
    all_names = get_db_names('both')
    if convert_type == 'udb_to_db':
        all_names = {all_names[dbname]: dbname for dbname in all_names}
        return all_names.get(name, '')
    elif convert_type == 'db_to_udb':
        return all_names.get(name, '')
    return ''

def nid_to_notes(db: 'Database', nid_list: list[int]) -> list[dict]:
    ' Convert notes nids to notes '
    notes_list: list = []
    for nid in nid_list:
        notes_list.append(db.get_by_nid(nid))
    return notes_list

def db_file_exist(dbname: str) -> bool:
    for file in os.listdir('./db/'):
        filename, ext = file.split('.')
        if filename == dbname:
            return True
    return False


class DBException(Exception):
    pass