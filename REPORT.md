# Project 2

* TODO: Refactor to have either snakecase or camelcase

## Q1

Q1 is divided into different sub-parts: WAV-related, UI-related and compressor-related.

## Compression ratio

While the compression ratios of LZW are better, it does not show the impact of having to pack the dictionary into the file.

_Create a map of my implementation (classes, modules). Describe the interface of all objects._

| Filename  | Huffman | LZW    | LZW-based Huffman | Huffman-based LZW |
| --------- | ------- | ------ | ----------------- | ----------------- |
| Car horn  | 1.5638  | 5.1213 |                   |                   |
| Explosion | 1.1753  | 3.7733 |                   |                   |
| Fire      | 1.1797  | 4.0152 |                   |                   |
| Leopard   | 1.3856  | 4.5684 |                   |                   |
| Wav8bit   | 1.3462  | 4.6984 |                   |                   |



## Q2

Apply GMM on image before lossy compression.

## References

* [Comparative data compression techniques and multi-compression results](https://iopscience.iop.org/article/10.1088/1757-899X/53/1/012081/pdf)