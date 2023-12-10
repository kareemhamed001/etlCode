from app.etl.updatedEtl import etl
DataOp = {
    'operation_type': 'train',
    'source': 'folder::e:\\python\\4rt grade first term\\compilers\\frames',
    'destination': 'folder::e:\\python\\4rt grade first term\\compilers\\frames\\acute_myna_object_novelty_ta_1_reo',
    'epoch': 20,
    'batchsize': 10,
    'model': 'vgg16',
}
DataSoruce = etl('folder::e:\\python\\4rt grade first term\\compilers\\frames\\acute_myna_object_novelty_ta_1_reo', 'folder::e:\\python\\4rt grade first term\\compilers\\frames', DataOp)
DataSoruce.Start()