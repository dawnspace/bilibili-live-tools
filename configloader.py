#!/usr/bin/env python3
# -*-coding:utf-8 -*-
import configparser
import codecs

def load_bilibili(file):
    cf_bilibili = configparser.ConfigParser()
    cf_bilibili.optionxform = str
    cf_bilibili.read_file(codecs.open(file, "r", "utf8"))
    dic_bilibili = cf_bilibili._sections
    dic_nomalised_bilibili = dic_bilibili['normal'].copy()
    dic_nomalised_bilibili['saved-session'] = dic_bilibili['saved-session'].copy()
    dic_nomalised_bilibili['account'] = dic_bilibili['account'].copy()
    if dic_nomalised_bilibili['account']['username']:
        pass
    else:
        username = input("# 输入帐号: ")
        password = input("# 输入密码: ")
        cf_bilibili.set('account', 'username', username)
        cf_bilibili.set('account', 'password', password)
        cf_bilibili.write(codecs.open(file, "w+", "utf8"))
        dic_nomalised_bilibili['account']['username'] = username
        dic_nomalised_bilibili['account']['password'] = password
    dic_bilibili_type = dic_bilibili['types']
    # str to int
    for i in dic_bilibili_type['int'].split():
        dic_nomalised_bilibili[i] = int(dic_bilibili['normal'][i])
    for i in dic_bilibili.keys():
        # print(i)
        if i[0:3] == 'dic':
            dic_nomalised_bilibili[i[4:]] = dic_bilibili[i]
    return dic_nomalised_bilibili


def load_user(file):
    cf_user = configparser.ConfigParser()
    cf_user.read_file(codecs.open(file, "r", "utf8"))
    dic_user = cf_user._sections
    return dic_user


def write2bilibili(dic):
    cf_bilibili = configparser.ConfigParser(interpolation=None)
    cf_bilibili.optionxform = str

    cf_bilibili.read_file(codecs.open("conf/bilibili.conf", "r", "utf8"))

    for i in dic.keys():
        cf_bilibili.set('saved-session', i, dic[i])

    cf_bilibili.write(codecs.open("conf/bilibili.conf", "w+", "utf8"))


def get_conf(file, section: str = None, option: str = None, interpolation: str = 'basic', contain_default: bool = False,
             option_type: str = None, raw: bool = False, _vars: dict = None, fallback=None):
    """
    获取配置文件
    :param file: 配置文件
    :param section: 配置文件的节名称
    :param option: 配置文件指定节的选项名称
    :param interpolation: 是否使用插入值转换，可选值:None, 'basic', 'extend'
    :param contain_default: 在不指定节名称和选项名称时，返回的整个配置文件中是否包含默认节
    :param option_type: 指定选项时获得指定类型选项，可选值：'int', 'float', 'bool', 'boolean'
    :param raw: 指定节名称和选项名称时，是否返回不扩展插入值的选项原本值
    :param _vars: 指定节名称和选项名称时，在_vars字典中搜索指定选项
    :param fallback: 指定节名称和选项名称时，未搜到选项时返回fallback的值
    :return:
    """
    if interpolation:
        _interpolation = str(interpolation).lower().strip()
        if _interpolation == 'basic':
            interpolation = configparser.BasicInterpolation()
        elif _interpolation == 'extend':
            interpolation = configparser.ExtendedInterpolation()
        else:
            interpolation = None
    else:
        interpolation = None

    conf = configparser.ConfigParser(allow_no_value=True, interpolation=interpolation)
    conf.optionxform = str
    with codecs.open(file, "r", "utf8") as fr:
        conf.read_file(fr)

    if not section:
        tmp = dict(conf.items())

        if not contain_default:
            del tmp['DEFAULT']

        for _t in tmp.keys():
            tmp[_t] = dict(tmp[_t])
        return tmp
    elif section and not option:
        return dict(conf.items(section))
    elif section and option:
        if option_type:
            _option_type = str(option_type).lower().strip()
            if _option_type in ['int', 'float', 'bool', 'boolean']:
                if _option_type == 'int':
                    return conf.getint(section, option, raw=raw, vars=_vars, fallback=fallback)
                elif _option_type == 'float':
                    return conf.getfloat(section, option, raw=raw, vars=_vars, fallback=fallback)
                else:
                    return conf.getboolean(section, option, raw=raw, vars=_vars, fallback=fallback)
        return conf.get(section, option, raw=raw, vars=_vars, fallback=fallback)
    else:
        return None


def set_conf(file, section: str, option: str = None, value=None, set_mode: str = 'set', set_dict: dict = None,
             skip_input: bool = True):
    """
    设置配置文件
    :param file: 配置文件
    :param section: 要设置的节
    :param option: 要设置的选项
    :param value: 要设置的选项的值
    :param set_mode: 设置配置文件的方式，可选值：'set','del','input'
    :param set_dict: 要设置的节中包含的选项和值
    :param skip_input: 当set_mode为input时，如果指定option或set_dict中的键所对应的值存在时是否跳过输入
    :return:
    """
    _set_mode = str(set_mode).lower().strip()
    if _set_mode not in ['set', 'del', 'input']:
        return

    conf = configparser.ConfigParser(allow_no_value=True, interpolation=None)
    conf.optionxform = str
    with codecs.open(file, "r", "utf8") as fr:
        conf.read_file(fr)

    if _set_mode == 'set':
        if not conf.has_section(section):
            conf.add_section(section)

        if option and value:
            conf.set(section, option, value)
        elif set_dict:
            if isinstance(set_dict, dict):
                for i in set_dict.keys():
                    conf.set(section, i, set_dict[i])
            else:
                raise TypeError('set_dict must be a dictionary') from None
    elif _set_mode == 'del':
        if section and not option:
            conf.remove_section(section)
        elif section and option:
            conf.remove_option(section, option)
    else:
        if option:
            if skip_input:
                _v = conf.get(section, option)
                if _v:
                    return _v

            v = input(f"Please enter {option}: ")
            conf.set(section, option, v)
        elif set_dict:
            if isinstance(set_dict, dict):
                if skip_input:
                    _dict = dict(conf.items(section))
                    if list(_dict.values())[0]:
                        return _dict

                for i in set_dict.keys():
                    set_dict[i] = input(f"Please enter {i}: ")
                    conf.set(section, i, set_dict[i])
            else:
                raise TypeError('set_dict must be a dictionary') from None

    with codecs.open(file, "w+", "utf8") as fw:
        conf.write(fw)
    return True
