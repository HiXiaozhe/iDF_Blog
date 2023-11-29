import time
import re

from rchain.client import RClient
from rchain.util import create_deploy_data, verify_deploy_data
from rchain.crypto import PrivateKey

from RChainAPI import config  # 配置文件

private_key = PrivateKey.from_hex(config.RCHAIN_KEY)  # 私钥
public_key = private_key.get_public_key()  # 公钥
ip = config.RCHAIN_IP  # ip
port = config.RCHAIN_PORT  # 端口


def return_data_list() -> list[str]:
    """
    返回已部署数据
    """
    with RClient(ip, port) as client:
        blockhash_list = [i.blockHash for i in client.get_blocks_by_heights(
            start_block_number=1,
            end_block_number=client.show_blocks()[0].blockNumber
        )
                          ]
        data_list = []
        for i in blockhash_list:
            block_info = client.show_block(i)
            data = extract_quotes(block_info.deploys[0].term)
            data_list.append(data[0])

    return data_list


def extract_quotes(string: str) -> list[str]:
    """
    正则表达式提取数据
    """
    pattern = r"!\(\"(.*?)\"\)"
    quotes = re.findall(pattern, string)
    return quotes


def func_deploy(rho_code: str) -> str:
    """
    智能合约的部署
    :param rho_code: 合约内容（str）
    :return: 返回读取到的数据
    """
    timestamp = int(time.time()) * 1000  # 时间戳

    client = RClient(ip, port)

    unforgeable_name = client.previewPrivateNames(public_key, timestamp, 1)  # 唯一名称
    print('Prepare Deploy...' + '\n')
    print('UnforgeableName:')
    print(unforgeable_name.payload, end='\n')

    valid_after_block_number = client.show_blocks()[0].blockNumber  # 最新区块

    deploy_data = create_deploy_data(
        timestamp_millis=timestamp,
        term=rho_code,
        key=private_key,
        phlo_limit=100000,
        phlo_price=1,
        valid_after_block_no=valid_after_block_number
    )

    verify_deploy_data(key=public_key, sig=deploy_data.sig, data=deploy_data)

    deploy_id = client.send_deploy(deploy_data)  # 部署
    print('deployResponse:')
    print('Success!')
    print('deployId:' + deploy_id + '\n')

    client.propose()
    print('Propose...' + '\n')

    time.sleep(3)  # 等待部署结果
    print('Propose Success!' + '\n')

    light_blockinfo = client.find_deploy(deploy_id)  # 返回部署结果
    print('DeployInfo:')
    print(light_blockinfo)

    ret = ''

    blockinfo = client.show_block(light_blockinfo.blockHash)
    data = extract_quotes(blockinfo.deploys[0].term)
    print('data:')
    print(data[0] + '\n')

    ret = data[0]  # 提取到的数据

    print('Deploy Finished!\n')
    return ret


def func_deploy_fromfile(rho_file: str) -> str:
    """
    智能合约的部署（文件版本）
    :param rho_file: 智能合约文件
    :return: 返回读取到的数据
    """
    with open(rho_file, 'r') as f:
        rho_code = f.read()
    return func_deploy(rho_code)


if __name__ == "__main__":
    contract = '''
    new hello in {
        hello!("welcome!")
    }
    '''

    # print('message=' + func_deploy(contract) + '\n')
    # print('message=' + func_deploy_fromfile('hello.rho') + '\n')
