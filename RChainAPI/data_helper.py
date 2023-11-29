from RChainAPI import rho_deploy


def select() -> list[str]:
    """
    查找数据
    :return: 返回数据列表
    """
    data_list = rho_deploy.return_data_list()
    return data_list


def insert(str_to_insert: str) -> None:
    """
    插入数据
    :param str_to_insert: 需要插入的数据
    :return: None
    """
    contract = '''
    new getInfo, setInfo in {{
        @{{"global_factory"}}!(*getInfo, *setInfo)
        |
        setInfo!("{}")
    }}
    '''.format(str_to_insert)

    rho_deploy.func_deploy(contract)


if __name__ == '__main__':
    insert("Hello world!")
    print(select())
