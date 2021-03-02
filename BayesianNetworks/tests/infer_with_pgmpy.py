import os
from pgmpy.readwrite import BIFReader
from pgmpy.inference import VariableElimination

def set_reader_location(file_path):
    reader = BIFReader(file_path)
    network = reader.get_model()
    infer = VariableElimination(network)
    return infer

if __name__ == '__main__':
    '''
    infer = set_reader_location('../bif_files/asia.bif')
    q = infer.query(variables=['bronc'], evidence={'smoke': 'no'})
    print(q)
    '''

    infer = set_reader_location('../bif_files/asia.bif')
    # a = infer.query(variables=['BirthAsphyxia'], evidence={'LowerBodyO2': '<5', 'RUQO2': '12+', 'CO2Report': '>=7.5', 'XrayReport': 'Asy/Patchy'})
    # b = infer.query(variables=['HypDistrib'], evidence={'LowerBodyO2': '<5', 'RUQO2': '12+', 'CO2Report': '>=7.5', 'XrayReport': 'Asy/Patchy'})
    # c = infer.query(variables=['HypoxiaInO2'], evidence={'LowerBodyO2': '<5', 'RUQO2': '12+', 'CO2Report': '>=7.5', 'XrayReport': 'Asy/Patchy'})
    # d = infer.query(variables=['CO2'], evidence={'LowerBodyO2': '<5', 'RUQO2': '12+', 'CO2Report': '>=7.5', 'XrayReport': 'Asy/Patchy'})
    # e = infer.query(variables=['ChestXray'], evidence={'LowerBodyO2': '<5', 'RUQO2': '12+', 'CO2Report': '>=7.5', 'XrayReport': 'Asy/Patchy'})
    # f = infer.query(variables=['Grunting'], evidence={'LowerBodyO2': '<5', 'RUQO2': '12+', 'CO2Report': '>=7.5', 'XrayReport': 'Asy/Patchy'})
    # g = infer.query(variables=['LVHreport'], evidence={'LowerBodyO2': '<5', 'RUQO2': '12+', 'CO2Report': '>=7.5', 'XrayReport': 'Asy/Patchy'})
    # h = infer.query(variables=['Disease'], evidence={'LowerBodyO2': '<5', 'RUQO2': '12+', 'CO2Report': '>=7.5', 'XrayReport': 'Asy/Patchy'})
    # i = infer.query(variables=['GruntingReport'], evidence={'LowerBodyO2': '<5', 'RUQO2': '12+', 'CO2Report': '>=7.5', 'XrayReport': 'Asy/Patchy'})
    # j = infer.query(variables=['Age'], evidence={'LowerBodyO2': '<5', 'RUQO2': '12+', 'CO2Report': '>=7.5', 'XrayReport': 'Asy/Patchy'})
    # k = infer.query(variables=['LVH'], evidence={'LowerBodyO2': '<5', 'RUQO2': '12+', 'CO2Report': '>=7.5', 'XrayReport': 'Asy/Patchy'})
    # l = infer.query(variables=['DuctFlow'], evidence={'LowerBodyO2': '<5', 'RUQO2': '12+', 'CO2Report': '>=7.5', 'XrayReport': 'Asy/Patchy'})
    # m = infer.query(variables=['CardiacMixing'], evidence={'LowerBodyO2': '<5', 'RUQO2': '12+', 'CO2Report': '>=7.5', 'XrayReport': 'Asy/Patchy'})
    # n = infer.query(variables=['LungParench'], evidence={'LowerBodyO2': '<5', 'RUQO2': '12+', 'CO2Report': '>=7.5', 'XrayReport': 'Asy/Patchy'})
    # o = infer.query(variables=['LungFlow'], evidence={'LowerBodyO2': '<5', 'RUQO2': '12+', 'CO2Report': '>=7.5', 'XrayReport': 'Asy/Patchy'})
    # p = infer.query(variables=['Sick'], evidence={'LowerBodyO2': '<5', 'RUQO2': '12+', 'CO2Report': '>=7.5', 'XrayReport': 'Asy/Patchy'})
    # print(a)
    # print(b)
    # print(c)
    # print(d)
    # print(e)
    # print(f)
    # print(g)
    # print(h)
    # print(i)
    # print(j)
    # print(k)
    # print(l)
    # print(m)
    # print(n)
    # print(o)
    # print(p)


    a = infer.query(variables=['either'], evidence={'bronc': 'yes', 'asia': 'yes'})
    print(a)
