# -*- coding: utf-8 -*-

try:
    from PySide import QtWidgets
except:
    from PyQt5 import QtWidgets

from azure.cosmosdb.table.tableservice import TableService
from azure.cosmosdb.table.models import Entity
from azure.cosmosdb.table.tablebatch import TableBatch
from ctypes import *
user32 = windll.user32
import const
const.CONNECTION_STRING = 'DefaultEndpointsProtocol=https;AccountName=dbforfaceapitest;AccountKey=fNpt9FKY2FjKa0q1ANN7KT9Gn/s2c8NY1gB8jenN9jqide2eWdz+zw8rX6RlU+DmSLW4tVvLpvyUUnPFhaH6PQ==;EndpointSuffix=core.windows.net'

class MyCosmosDB:
    def __init__(self):
        pass

    #----------------------------------------------
    # （内部処理）座席情報取得
    #----------------------------------------------
    def getDeskStatusTable(floorId, floorId_sat):
        try:

            # Azure Cosmos DB への接続（接続文字列を設定）
            table_service = TableService(connection_string=const.CONNECTION_STRING)

            # エンティティを照会する
            desks = table_service.query_entities('deskStatusTable', filter="PartitionKey eq 'deskId'")

            result = []
            for desk in desks:
                if desk['floorId']==floorId or desk['floorId']==floorId_sat or desk['floorId']=='999':
                    result.append(desk)

            return result

        except Exception as e:
            user32.MessageBoxW(0, '{0}:{1}'.format('getDeskStatusTable',e.args[0]), u'ERROR', 0x00000010)
            return None


    #----------------------------------------------
    # （内部処理）自席情報更新
    #----------------------------------------------
    def updateDeskStatus(deskId, userId, userName, statusCd):
        try:

            # Azure Cosmos DB への接続（接続文字列を設定）
            table_service = TableService(connection_string=const.CONNECTION_STRING)

            # エンティティを更新する
            entity = Entity()
            entity.PartitionKey = 'deskId'
            entity.RowKey = deskId
            entity.userId = userId
            entity.userName = userName
            entity.statusCd = statusCd
            table_service.merge_entity('deskStatusTable', entity, if_match='*')

        except Exception as e:
            user32.MessageBoxW(0, '{0}:{1}'.format('updateDeskStatus',e.args[0]), u'ERROR', 0x00000010)
            return None
