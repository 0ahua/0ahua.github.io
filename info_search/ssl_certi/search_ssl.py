from OpenSSL import SSL, crypto
import socket


def get_certificate_info(hostname, port=443):
    context = SSL.Context(SSL.TLSv1_2_METHOD)
    conn = SSL.Connection(context, socket.socket(socket.AF_INET, socket.SOCK_STREAM))
    conn.connect((hostname, port))
    conn.set_tlsext_host_name(hostname.encode())
    conn.do_handshake()

    cert = conn.get_peer_certificate()

    print(f"Subject: {cert.get_subject().CN}")
    print(f"Issuer: {cert.get_issuer().CN}")

    pem_cert = crypto.dump_certificate(crypto.FILETYPE_PEM, cert).decode()
    print(pem_cert)

    conn.shutdown()
    conn.close()

    # Write certificate information to ssl_certi.txt file
    with open("E:\python\FinalProject\info_search\\result\ssl_certi.txt", "w", encoding='utf-8') as file:
        file.write(f"Subject: {cert.get_subject().CN}\n")
        file.write(f"Issuer: {cert.get_issuer().CN}\n")
        file.write(pem_cert)

    print("Certificate information has been written to ssl_certi.txt file.")


# Example usage
hostname = "jd.com"  # Replace with your hostname
port = 443  # Replace with the desired port

get_certificate_info(hostname, port)