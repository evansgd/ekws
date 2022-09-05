"""Command-line program to test a steganographic method to embed a key in a ciphertext"""
import sys
import argparse
import protocol

KEY_LENGTH_IN_BYTES = 48

def main():
    """Runs the POC"""
    parser = argparse.ArgumentParser(description='Embed a cryptographic key in ciphertext')
    parser.add_argument('--message', help='plain text message (utf-8)')
    parser.add_argument(
        '--loci',
         help="""shared secret consisting of a comma-separated list of \
                 all the positions in the ciphertext
                 where the sub-keys will be inserted (e.g p1,p2,...,pn)
              """
     )

    args = parser.parse_args()

    key_locations = [int(locus) for locus in args.loci.split(',') if locus.isdigit()]
    key_locations = list(dict.fromkeys(key_locations))
    if len(key_locations) < KEY_LENGTH_IN_BYTES:
        sys.exit(
            f"You need to have {KEY_LENGTH_IN_BYTES} loci. \
            You have {len(key_locations)} correct values only."
        )

    i_protocol = protocol.Protocol(key_locations)
    cipher_text_with_embed_key = i_protocol.send(args.message)
    retrieved_key, retrieved_message = i_protocol.receive(cipher_text_with_embed_key)

    print(f'Key extracted from ciphertext is: \n {retrieved_key}')
    yes_or_no = "yes" if args.message == retrieved_message else "no"
    print(f'Is input message same as output message?: {yes_or_no}')

if __name__ == "__main__":
    main()
