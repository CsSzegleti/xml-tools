#!/bin/python3

import sys


class Field:
    def __init__(self, field_type: str, name: str):
        self.type = field_type
        self.name = name


def print_string_field(field_name: str) -> None:
    print(f'\t<field name="{field_name}" class="java.lang.String"/>')


def print_bool_field(field_name: str) -> None:
    print(f'\t<field name="{field_name}" class="java.lang.Boolean"/>')


def print_integer_field(field_name: str) -> None:
    print(f'\t<field name="{field_name}" class="java.lang.Integer"/>')


def print_long_field(field_name: str) -> None:
    print(f'\t<field name="{field_name}" class="java.lang.Long"/>')

def print_double_field(field_name: str) -> None:
    print(f'\t<field name="{field_name}" class="java.lang.Double"/>')


def print_date_field(field_name: str) -> None:
    print(f'\t<field name="{field_name}" class="java.util.Date"/>')


def print_field(field: Field) -> None:
    if field.type == 'String':
        print_string_field(field.name)
    elif field.type == "Integer":
        print_integer_field(field.name)
    elif field.type == "Long":
        print_long_field(field.name)
    elif field.type == "Boolean":
        print_bool_field(field.name)
    elif field.type == "Date":
        print_date_field(field.name)
    elif field.type == "Double":
        print_date_field(field.name)


def print_fields(class_fields: [Field]) -> None:
    for field in class_fields:
        print_field(field)


if __name__ == '__main__':
    if len(sys.argv) < 2 and not sys.argv[1].endswith(".java"):
        raise Exception("Not a java file!")

    java_file = sys.argv[1]

    fields = []
    with open(java_file, "r") as java:
        for line in java:
            line = line.strip().split("//")
            if line[0].startswith("private") and not line[0].startswith("private static final long serialVersionUID"):
                field_declaration = line[0].strip()[:-1].split(" ")
                fields.append(
                    Field(field_declaration[1], field_declaration[2]))

    print_fields(fields)
