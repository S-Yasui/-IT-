# -*- coding: utf-8 -*-

from azure.cosmosdb.table.tableservice import TableService
from azure.cosmosdb.table.models import Entity
from azure.cosmosdb.table.tablebatch import TableBatch

# Azure Cosmos DB への接続（接続文字列を設定）
table_service = TableService(connection_string='DefaultEndpointsProtocol=https;AccountName=dbforfaceapitest;AccountKey=fNpt9FKY2FjKa0q1ANN7KT9Gn/s2c8NY1gB8jenN9jqide2eWdz+zw8rX6RlU+DmSLW4tVvLpvyUUnPFhaH6PQ==;EndpointSuffix=core.windows.net')

'''
# テーブルを作成する
table_service.create_table('deskStatusTable')

# エンティティをテーブルに追加する
entity = Entity()
entity.PartitionKey = 'userId'
entity.RowKey = 'S7223'
entity.userName = '安井誠良'
table_service.insert_entity('userMaster', entity)


# エンティティをまとめてテーブルに追加する
batch = TableBatch()
desk001 = {'PartitionKey': 'deskId', 'RowKey':'0000001', 'floorId':'017', 'x':170, 'y':180, 'userId':'', 'userName':'', 'statusCd':''}
desk002 = {'PartitionKey': 'deskId', 'RowKey':'0000002', 'floorId':'017', 'x':170, 'y':270, 'userId':'A001', 'userName':'高橋加奈', 'statusCd':'1'}
desk003 = {'PartitionKey': 'deskId', 'RowKey':'0000003', 'floorId':'017', 'x':170, 'y':360, 'userId':'', 'userName':'', 'statusCd':''}
desk004 = {'PartitionKey': 'deskId', 'RowKey':'0000004', 'floorId':'017', 'x':170, 'y':450, 'userId':'A002', 'userName':'山口良太', 'statusCd':'3'}
desk005 = {'PartitionKey': 'deskId', 'RowKey':'0000005', 'floorId':'017', 'x':260, 'y':180, 'userId':'S7223', 'userName':'安井誠良', 'statusCd':'2'}
desk006 = {'PartitionKey': 'deskId', 'RowKey':'0000006', 'floorId':'017', 'x':260, 'y':270, 'userId':'', 'userName':'', 'statusCd':''}
desk007 = {'PartitionKey': 'deskId', 'RowKey':'0000007', 'floorId':'017', 'x':260, 'y':360, 'userId':'A003', 'userName':'金森祐', 'statusCd':'4'}
desk008 = {'PartitionKey': 'deskId', 'RowKey':'0000008', 'floorId':'017', 'x':260, 'y':450, 'userId':'', 'userName':'', 'statusCd':''}

batch.insert_entity(desk001)
batch.insert_entity(desk002)
batch.insert_entity(desk003)
batch.insert_entity(desk004)
batch.insert_entity(desk005)
batch.insert_entity(desk006)
batch.insert_entity(desk007)
batch.insert_entity(desk008)

table_service.commit_batch('deskStatusTable', batch)
'''

# エンティティをまとめて更新する
batch = TableBatch()
desk001 = {'PartitionKey': 'deskId', 'RowKey':'0000001', 'floorId':'017', 'x':170, 'y':60, 'userId':'A001', 'userName':'高橋加奈', 'statusCd':'2'}
desk002 = {'PartitionKey': 'deskId', 'RowKey':'0000002', 'floorId':'017', 'x':170, 'y':110, 'userId':'', 'userName':'', 'statusCd':''}
desk003 = {'PartitionKey': 'deskId', 'RowKey':'0000003', 'floorId':'017', 'x':170, 'y':170, 'userId':'', 'userName':'', 'statusCd':''}
desk004 = {'PartitionKey': 'deskId', 'RowKey':'0000004', 'floorId':'017', 'x':170, 'y':220, 'userId':'', 'userName':'', 'statusCd':''}
desk005 = {'PartitionKey': 'deskId', 'RowKey':'0000005', 'floorId':'017', 'x':260, 'y':60, 'userId':'', 'userName':'', 'statusCd':''}
desk006 = {'PartitionKey': 'deskId', 'RowKey':'0000006', 'floorId':'017', 'x':260, 'y':110, 'userId':'', 'userName':'', 'statusCd':''}
desk007 = {'PartitionKey': 'deskId', 'RowKey':'0000007', 'floorId':'017', 'x':260, 'y':170, 'userId':'', 'userName':'', 'statusCd':''}
desk008 = {'PartitionKey': 'deskId', 'RowKey':'0000008', 'floorId':'017', 'x':260, 'y':220, 'userId':'', 'userName':'', 'statusCd':''}

batch.insert_or_replace_entity(desk001)
batch.insert_or_replace_entity(desk002)
batch.insert_or_replace_entity(desk003)
batch.insert_or_replace_entity(desk004)
batch.insert_or_replace_entity(desk005)
batch.insert_or_replace_entity(desk006)
batch.insert_or_replace_entity(desk007)
batch.insert_or_replace_entity(desk008)

table_service.commit_batch('deskStatusTable', batch)

'''
# エンティティを更新する
entity = Entity()
entity.PartitionKey = 'deskId'
entity.RowKey = '0000001'
entity.floorId = '017'
entity.userId = 'A001'
entity.userName = '高橋加奈'
entity.statusCd = '2'
table_service.merge_entity('deskStatusTable', entity, if_match="*")
'''

statusList = {'1':'在席', '2':'話し中', '3':'トラブル発生', '4':'離席中'}

# エンティティを照会する
desks = table_service.query_entities('deskStatusTable', filter="PartitionKey eq 'deskId'")
for desk in desks:
    status = '不明'
    if len(desk['statusCd'])>0:
        status = statusList[desk['statusCd']]

    print('deskId:{0}, userName:{1}, status:{2}'.format(desk['RowKey'], desk['userName'], status))
