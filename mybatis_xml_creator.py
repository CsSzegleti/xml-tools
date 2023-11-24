#!/bin/python3

import sys


class Field:
    def __init__(self, field_type: str, name: str, column: str):
        self.type = field_type
        self.name = name
        self.column = column


def print_string_search(field_name: str, column_name: str) -> None:
    print(f'\t\t\t<if test="request.{field_name} != null">')
    print(f'\t\t\t\tAND {column_name} LIKE #{{request.{field_name}}}')
    print(f'\t\t\t</if>')


def print_bool_search(field_name: str, column_name: str) -> None:
    print(f'\t\t\t<if test="request.{field_name} != null">')
    print(f'\t\t\t\tAND {column_name} = #{{request.{field_name}, javaType=java.lang.Boolean, jdbcType=NUMERIC, typeHandler=hu.danubia.partnerservice.mapper.FlagHandler}}')
    print(f'\t\t\t</if>')


def print_range_search(field_name: str, column_name: str) -> None:
    print(f'\t\t\t<if test="request.{field_name} != null and request.{field_name}.from != null">')
    print(f'\t\t\t\tAND {column_name} >= #{{request.{field_name}.from}}')
    print(f'\t\t\t</if>')
    print(f'\t\t\t<if test="request.{field_name} != null and request.{field_name}.until != null">')
    print(f'\t\t\t\t<![CDATA[AND {column_name} <= #{{request.{field_name}.until}}]]>')
    print(f'\t\t\t</if>')


def print_date_search(field_name: str, column_name: str) -> None:
    print(f'\t\t\t<if test="request.{field_name} != null and request.{field_name}.from != null">')
    print(f'\t\t\t\tAND {column_name} >= #{{request.{field_name}.from,javaType=Date,jdbcType=DATE}}')
    print(f'\t\t\t</if>')
    print(f'\t\t\t<if test="request.{field_name} != null and request.{field_name}.until != null">')
    print(f'\t\t\t\t<![CDATA[AND {column_name} <= #{{request.{field_name}.until,javaType=Date,jdbcType=DATE}}]]>')
    print(f'\t\t\t</if>')


def print_search(field: Field) -> None:
    if field.type == 'String':
        print_string_search(field.name, field.column)
    elif field.type == "Integer" or field.type == "Double":
        print_range_search(field.name, field.column)
    elif field.type == "Boolean":
        print_bool_search(field.name, field.column)
    elif field.type == "Date":
        print_date_search(field.name, field.column)


def print_orderBy(field: Field) -> None:
    print(f'\t\t\t\t<when test="request.sortBy.compareTo(\'{field.name}\') == 0">')
    print(f'\t\t\t\t\tORDER BY {field.column}')
    print(f'\t\t\t\t</when>')


def print_select(java_class_name: str, class_fields: [Field]) -> None:
    print(f'\t<select id="{method_name}" parameterType="map" resultMap="{java_class_name + "Result"}">')
    print(f'\t\tSELECT * FROM DANUBIA.{table_name}')
    print('\t\t<where>')
    print('\t\t\t1=1')
    for field in class_fields:
        print_search(field)
    print('\t\t</where>')
    print(f'\t\t<if test="request.sortBy != null and request.sortBy.compareTo(\'undefined\') != 0">')
    print(f'\t\t\t<choose>')
    for field in class_fields:
        print_orderBy(field)
    print('\t\t\t\t<otherwise>')
    print('\t\t\t\t</otherwise>')
    print(f'\t\t\t</choose>')
    print('\t\t\t<if test="mainPartnerRequest.sortAscending != null">')
    print('\t\t\t\t<choose>')
    print('\t\t\t\t\t<when test="request.sortAscending.compareTo(true) == 0">')
    print('\t\t\t\t\t\tASC')
    print('\t\t\t\t\t</when>')
    print('\t\t\t\t\t<otherwise>')
    print('\t\t\t\t\t\tDESC')
    print('\t\t\t\t\t</otherwise>')
    print('\t\t\t\t</choose>')
    print('\t\t\t</if>')
    print('\t\t</if>')
    print('\t</select>')


def print_field_map(field: Field):
    print(f'\t\t\t<result property="{field.name}" column="{field.column}" />')


def print_result_map(java_package_name: str, java_class_name: str, class_fields: [Field]) -> None:
    print(f'\t\t<resultMap id="{java_class_name}Result" type="{java_package_name}.{java_class_name}">')
    for field in class_fields:
        print_field_map(field)
    print('\t\t</resultMap>')



if __name__ == '__main__':
    if len(sys.argv) < 2 and not sys.argv[1].endswith(".java"):
        raise Exception("Not a java file!")

    if len(sys.argv) < 3:
        raise Exception("No method name!")

    if len(sys.argv) < 4:
        raise Exception("No table name")

    method_name = sys.argv[2]
    java_file = sys.argv[1]
    table_name = sys.argv[3]

    fields = []
    with open(java_file, "r") as java:
        for line in java:
            line = line.strip().split("//")
            if line[0].startswith("public class"):
                class_name = line[0].split(" ")[2]
            elif line[0].startswith("package"):
                package_name = line[0].split(" ")[1][:-1]
            elif line[0].startswith("private") and not line[0].startswith("private static final long serialVersionUID"):
                field_declaration = line[0].strip()[:-1].split(" ")
                fields.append(Field(field_declaration[1], field_declaration[2], line[1].strip()))

    print_result_map(package_name, class_name, fields)
    print_select(class_name, fields)
