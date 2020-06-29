from recipes.rfc7636_challenge_generator import __recipe__

import click


@click.command()
@click.option('--code-verifier', '-c', required=True,
              help='Code verifier string')
def main(code_verifier):  # noqa: D101
    code_challenge = __recipe__.calculate_code_challenge(code_verifier)
    print(code_challenge)
    # print('SHA        {}\nB64        {}\nB64-STRIP  {}\nCC         {}'.format(
    #     sha,
    #     b64.decode('utf-8'),
    #     b64_strip.decode('utf-8'),
    #     code_challenge
    # ))


if __name__ == '__main__':
    main()
