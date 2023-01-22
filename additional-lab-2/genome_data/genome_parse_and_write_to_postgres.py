import psycopg
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("--host", help="postgres host", required=True)
parser.add_argument("--port", help="postgres port", required=False, default=5432)
parser.add_argument("--user", help="postgres user", required=True)
parser.add_argument("--password", help="postgres password", required=True)
parser.add_argument("--database", help="postgres database", required=True)
parser.description = """
example:
python .\genome_parse_and_write_to_postgres.py --host="192.168.56.105" --user="user_course" --password="F@ke_P@55" --database "db_course"
"""

args = parser.parse_args()


def get_sequence_from_genome_file(genome_file_path: str, k: int):
    with open(genome_file_path, "r") as genome_file:
        genome = genome_file.read().replace("\n", "")
        last_element_position = len(genome) - k + 1
        sequence = [genome[i : i + k] for i in range(0, last_element_position)]
    return sequence


def write_sequence_to_postgres(sequence: list, genome: str, k: int):
    records = [(genome, k, i, sequence[i]) for i in range(0, len(sequence))]
    with psycopg.connect(
        user=args.user, password=args.password, host=args.host, port=args.port, dbname=args.database
    ) as conn:
        with conn.cursor() as cursor:
            with conn.transaction():
                with cursor.copy("COPY additional.genome_sequense (genome, k, index, element) FROM STDIN") as copy:
                    for record in records:
                        copy.write_row(record)


if __name__ == "__main__":
    jobs = [
        {"genome": "A", "file": "Genome_1-1.txt", "k": 2},
        {"genome": "A", "file": "Genome_1-1.txt", "k": 5},
        {"genome": "A", "file": "Genome_1-1.txt", "k": 9},
        {"genome": "B", "file": "Genome_2-1.txt", "k": 2},
        {"genome": "B", "file": "Genome_2-1.txt", "k": 5},
        {"genome": "B", "file": "Genome_2-1.txt", "k": 9},
    ]

    for job in jobs:
        genome = job["genome"]
        file_path = job["file"]
        k = job["k"]
        print(f"genome='{genome}' k={k}..")
        sequence = get_sequence_from_genome_file(genome_file_path=file_path, k=k)
        write_sequence_to_postgres(sequence, genome=genome, k=k)
