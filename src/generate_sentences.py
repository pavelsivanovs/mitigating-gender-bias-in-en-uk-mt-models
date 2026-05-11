import argparse
import csv
import logging

logger = logging.getLogger(__name__)

TEMPLATE_TOKEN = '<OCCUPATION>'


def generate_sentences(occupations: list[str], templates: list[dict]) -> list[dict]:
    sentences = []
    id = 1
    for occupation in occupations:
        for template in templates:
            sentence = template['template'].replace(TEMPLATE_TOKEN, occupation)
            sentences.append({
                'id': id,
                'template_type': template['id'],
                'occupation': occupation,
                'source': sentence,
                'source_gender': template['gender'],
            })
            id += 1
    logger.info(f'Generated {len(sentences)} test sentences.')
    return sentences


def main():
    logging.basicConfig(level=logging.INFO)
    parser = argparse.ArgumentParser()
    parser.add_argument('occupations_file')
    parser.add_argument('templates_file')
    parser.add_argument('-o', '--output_file', default='translations.tsv')
    args = parser.parse_args()

    with open(args.occupations_file, mode='r') as file:
        occupations = file.read().split('\n')
        logger.info(f'Read {len(occupations)} occupations: {', '.join(occupations[:5])}...')

    with open(args.templates_file, mode='r', newline='') as file:
        reader = csv.DictReader(file, delimiter='\t')
        templates = list(reader)
        logger.info(f'Read {len(templates)} sentence templates.')

    sentences = generate_sentences(occupations, templates)
    with open(args.output_file, mode='w', newline='') as file:
        fieldnames = ['id', 'template_type', 'occupation', 'source', 'source_gender']
        writer = csv.DictWriter(file, fieldnames, delimiter='\t')
        writer.writeheader()
        writer.writerows(sentences)
        logger.info(f'Wrote test sentences to {args.output_file}.')


if __name__ == '__main__':
    main()
