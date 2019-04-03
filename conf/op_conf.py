# coding: utf8
import os
import configparser


path = os.path.dirname(__file__) + '/setting.conf'
cf = configparser.ConfigParser()
cf.read(path)


def read_conf(section):
    lst = cf.items(section)
    return lst


def write_conf(section, option, value):
    cf.set(section, option, value)
    with open(path, "w+") as f:
        cf.write(f)


def chang_conf(dev):
    section = 'dev' if dev else 'prod'
    lst = read_conf(section)
    for v in lst:
        write_conf('conf', v[0], v[1])


def get_conf():
    lst = read_conf('conf')
    obj = dict()
    for v in lst:
        val = v[1]
        if v[0] in ['port', 'is_dev', 'jwt_expire']: val = int(v[1])
        obj[v[0]] = val
    return obj


if __name__ == '__main__':
    obj = get_conf()
    print(obj)