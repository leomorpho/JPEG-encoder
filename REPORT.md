# Project 2

* TODO: Refactor to have either snakecase or camelcase

## Q1

Q1 is divided into different sub-parts: WAV-related, UI-related and compressor-related.

### Bug correction

I corrected a significant bug that I did not even realize I had. Thanks to the marking feedback, I became aware of it. The sound wave now corresponds to the one shown by actual sound libraries.

### Compression ratio

While the compression ratios of LZW are better, it does not show the impact of having to pack the dictionary into the file.

_Create a map of my implementation (classes, modules). Describe the interface of all objects._

For the compression ratio, the input is translated to a list of short integers. The reason is that the audio files we are reading for this assignment would store [0-255] in a short integer. I therefore calculate the space it would take in regards to that (and not a 4 byte integer or float). To get the length in bytes of the encoded data, I divide the length of it by 8 for 8 bits/byte since the codes would be packed together.

The compression ratio only takes into account the payload of the sound file. The size of the Huffman tree itself is not taken into account even though a real file would need to have it stored for later decoding. Likewise, no table is saved to disk for the LZW compressed file.

| Filename  | Huffman  | LZW      | FLAC     |
| --------- | -------- | -------- | -------- |
| Car horn  | 1.21 : 1 | 4.03 : 1 | 1.81 : 1 |
| Explosion | 1.18 : 1 | 3.72 : 1 | 1.57 : 1 |
| Fire      | 1.20 : 1 | 4.04 : 1 | 1.63 : 1 |
| Leopard   | 1.32 : 1 | 4.20 : 1 | 2.04 : 1 |

From my research online, Huffman generally compresses at 1.5:1 and LZW at 5:1. My ratios are slightly below these. The sounds used for testing may have more entropy than the average, or else my code may have a bug. I tested my code extensively with an 81% code coverage in `pytests` tests.

Compared to the FLAC compression standard, my Huffman implementation had poorer performance but my LZW implementation had higher performance. From what I found on the internet, the FLAC compression ratio generally compresses at a 2:1 ratio. The FLAC compression ratios seen above are a little under that. However, that is consistent with the Huffman and LZW compression ratios being lower than the average (as found on the internet). Therefore, my code must be correct.

The Huffman encoder from Q1 was expanded in Q2 to be a full Huffman implementation:

* Creates Huffman tree
* Can encode a string to Huffman codes
* Can serialize the tree to bytes, and deserialize the tree from bytes (no libraries were used).

## Q2

The following implementation is an attempt at a simplified version of JPEG. It is simplified in that it supports only the BMP file specified within the assignment. It currently does not work perfectly, with the quality of the compressed image being much lower than expected. I was unable to debug this part, as the whole project was massive and took me about 80h and 5000 lines of code.

The color layers was not downsampled.

<img src="REPORT.assets/Screen%20Shot%202020-08-03%20at%205.17.04%20PM.png" alt="Example" width="600" >

The following steps were implemented:

* Separate RGB into YCbCr
  * Split each layer into 8x8 blocks
  * For every block:
    * DCT
    * Quantize
    * Zigzag entropy coding
    * Convert to bytes
* Serialize and deserialize Huffman tree

The opposite was implemented for decoding. Encoding and decoding were implemented at the same time. This made development easier as my `pytests` were just the opposite of one another. It was surprisingly challenging and fun to perform each step. 

#### How to use

* When opening a `bmp` file, the original as well as a 90% quality image will be displayed. The compressed copy of the original will be saved in the same directory as the original with the `img` extension.
* When opening a `img` file, the compressed image will be read from file and displayed.

### Colour transform

The conversion from RGB to YCbCr used values from [this wikipedia reference page](https://en.wikipedia.org/wiki/YCbCr).

### 2D Discrete Cosine Transform

The DCT of columns and rows were taken separately and then combined.

### Quantization

All the layers are quantized with the same quantization matrix. The more aggressive quantization for the chroma layer was not implemented here. The 50% tables were taken from the textbook. The 10% and 90% tables were taken from Wikipedia.

### Huffman encoding

| Method                   | Description                                                  |
| ------------------------ | ------------------------------------------------------------ |
| Encode(string)           | Encode data that has been converted to a string.             |
| Decode(string)           |                                                              |
| Serialize_tree           | A recursive function to serialize a Huffman tree. Every node is indicated by a `1`, a leaf is indicated by a `0`. A leaf is always followed by 2 bytes encoding the leaf value as a binary string literal (eg.: `00010100 001011001`) |
| Deserialize_tree         | Contains a recursive helper function to translate a binary string literal (`010011..`) into the correct Huffman tree |
| Create_tree              | Creates a Huffman tree from a list of nodes                  |
| Assign_codes             | Assigns codes recursively to the Huffman tree                |
| Create_prob_distribution | To create the Huffman tree, the probability distribution of the samples must be known. This function realizes this. It uses a hash table (dictionnary) to keep count of each sample. |
| Convert_samples_to_code  | Once the Huffman tree is built, this function can convert the samples to the compressed Huffman codes |

### Main JPEG methods

The `src/compression/lossy.py` holds the JPEG pipelines

| Method                                       | Description                                                  |
| -------------------------------------------- | ------------------------------------------------------------ |
| JPEG                                         | Converts a matrix representing an image into the JPEG format and writes the new file. It then reads from that file and returns the JPEG image (a matrix of pixels). |
| Read_JPEG                                    | Performs JPEG in reverse to read from file. The `JPEG` function (above) uses this function to read from file. |
| Separate_image_layers  and join_image_layers | The layers must be separated to be compressed. They then must be stitched back together to be displayed as a single image. |
| Block_split_layer and block_join_layer       | The JPEG pipeline is operated on a block basis. Blocks are 8x8 pixels from the original image. These were quite tricky to implement.s |
|                                              |                                                              |
|                                              |                                                              |
|                                              |                                                              |

### Zigzag encoding

The 8x8 blocks are zigzag encoded to place all the high coefficients together. In this manner, the zeroes are mostly all together and the whole vector can be compressed more efficiently.

| Method               | Description                                                  |
| -------------------- | ------------------------------------------------------------ |
| Zigzag and un zigzag | These are pretty self-explanatory. These were tricky to implement. Writing tests helped immensely. I am glad that I learned to write good test from my job! Test-driven development is a good habit. |



### Experimentation

When I tired running DCT and reverse DCT, these are the results. I was making the mistake of dequantizating after the reverse DCT.

![Screen Shot 2020-07-18 at 12.15.02 PM](REPORT.assets/Screen%20Shot%202020-07-18%20at%2012.15.02%20PM.png)

I think there is (was) a bug at that point, but the results were quite exciting, it's like psychadelic art!

In the next one, I had forgotten to add the difference of the DC coefficients (+128) back in during reverse DCT 

![Screen Shot 2020-07-18 at 12.25.04 PM](REPORT.assets/Screen%20Shot%202020-07-18%20at%2012.25.04%20PM.png)

Still not quite there yet. I am trying to find what I have done wrong. I have commented out the quantization steps. I am expecting to see an almost identical image to the original, since I am only running DCT on it.

![Screen Shot 2020-07-18 at 12.41.13 PM](REPORT.assets/Screen%20Shot%202020-07-18%20at%2012.41.13%20PM.png)

July 15: I tested to see if the previous step was much lighter because I was adding 128 to every pixel twice after DCT, but the pixels are clearly out of the [0, 255] bound now:

![Screen Shot 2020-07-18 at 12.44.28 PM](REPORT.assets/Screen%20Shot%202020-07-18%20at%2012.44.28%20PM.png)

I re-wrote my DCT steps as I am pretty confident my bug is there. I made sure to perform the following in order, and then in reverse for reverse DCT:

* Substract 128 for al values
* DCT for rows
* DCT for columns

July22 : Clearly, there is still something wrong. I do think there is an improvement, as the image is not overexposed anymore. 

![Screen Shot 2020-07-22 at 3.30.12 PM](REPORT.assets/Screen%20Shot%202020-07-22%20at%203.30.12%20PM.png)

I applied only the row DCT and adjusted the reverse DCT to set 0 if values were below zero. Looking better.

![Screen Shot 2020-07-22 at 3.36.05 PM](REPORT.assets/Screen%20Shot%202020-07-22%20at%203.36.05%20PM.png)

Adjusted the previous state to also apply column DCT. It is better than before. However, the quality is much lower. I wonder if that is caused by the naive DCT implementation. Otherwise, there is another bug.

![Screen Shot 2020-07-22 at 3.37.28 PM](REPORT.assets/Screen%20Shot%202020-07-22%20at%203.37.28%20PM.png)

Reapplying quantization for 90% quality yields a result which appears to be much lower than 90% of the original's quality.

![Screen Shot 2020-07-22 at 3.42.17 PM](REPORT.assets/Screen%20Shot%202020-07-22%20at%203.42.17%20PM.png)

Nearing the end of my project, I found and fixed some bugs. The great news was that my image finally improved to a quality I would expect for 90%!

![Screen Shot 2020-08-01 at 6.02.06 PM](REPORT.assets/Screen%20Shot%202020-08-01%20at%206.02.06%20PM.png)

### File size issues

I wonder if the enormous file size is introduced by utf8 encoding. Looking at the byte array, 2 bytes take the space of 16 bytes. There is therefore an issue with what should be a byte ending up being 8 times as large. Each bit is being encoded as a byte.

I did not think that I would be able to fix this size issue, but after finding out that each bit was encoded as a byte, i figured out how to correct it. I converted each string of binary ("11010010") to an integer, then wrote that integer as a single byte to file. I then read that integer and converted it to a binary string.

### File saving

The huffman tree is serialized to a string. For every node which has children, a "1" is appended. If the node has no children, a "0" is a appended, followed by a byte which represents the leaf's sample value.

Serializing and deserializing the Huffman tree was quite a challenge. The deserialization the most difficult of the two. It was hard to test that it worked. I tested by first serializing (since I could easily look at my serializer result), then I deserialized it, deserialized it, and compared the two serialized strings, making sure that they were equal.

I then found that the serialized tree represented the leaf values funily as the negative numbers had a minus sign preceding them. I had no prior experience working with bytes in python, so I had to do some research about how to deal with them. The leaves are stored as 2-byte signed integers. The 2-byte signed integer is formed from a 16-bit string (16 zeroes or ones). This quirk is due to how I serialize the Huffman tree. 

**Possible bug**: I can't quite put my finger on it, but my test `test_serialize` shows me that there is something fishy in my serializer/deserializer. If I run into any issues reading the tree from file, I should definitely assume that this part is responsible.

Indeed, when reading the serialized tree from file and attempting to deserialize it, negative signed integers were positive (for instance -94 was 32862). The error was due to me comparing the first char of the string to an integer and not a string... (`if string[0]== 1` instead of `if string[0]== "1"`). I made so many of these types of errors in this project, as well as many of by one erorrs. Unfortunately, they can sometimes be time consuming to debug.

#### File format

| Field             | Description                                 | Size             |
| ----------------- | ------------------------------------------- | ---------------- |
| Width             | width of the image in blocks                | 4 byte           |
| Height            | Height of the image in blocks               | 4 byte           |
| Block size        | Size of the blocks (default is 8x8)         | 4 byte           |
| Width in columns  | Width of the matrix in pixel columns        | 4 byte           |
| Compression       | Compression used                            | 4 byte           |
| Main data padding | How much padding in bytes the main data has | Variable (bytes) |
| Tree size         | Size of the Huffman tree in bytes           | Variable (bytes) |
| Tree padding      | How much padding in bytes the tree data has | Variable (bytes) |

There are instances in which I thought my API was confusing. If I had time, I would have refactored it.

| Method                                | Description                                                  |
| ------------------------------------- | ------------------------------------------------------------ |
| Encode                                | Encode a matrix representing an image into a vector.         |
| Decode                                | Decode a vector of values into an image. Huffman decoding happens here. |
| Write                                 | Write the encoded image                                      |
| Read                                  | Read the encoded image. Deserialize the Huffman tree         |
| Vector_to_layers and layers_to_vector | Convert between layers of an image and a single vector. The image is saved as a byte string, which is built from the vector. |
| Subdivide_layer and subdivide_row     | Separate a vector to layers, and separate a vector into rows. These is a helper function of the above functions. |
| Str_to_byte_array                     | The last step before writing to file: the vector representing the image is encoded into a byte array. |
| Pad_byte                              | Pad a binary string literal (`001`) so that it is a full byte (`00000001`) |



#### Run-length coding

The current implementation does not have run-length coding.

#### Reading from file

This was quite a challenging part. I think not having refactored my API made it more difficult. After much struggle, I succesfully got the image (or rather part of it) to show:

<img src="REPORT.assets/Screen%20Shot%202020-08-01%20at%204.14.35%20PM.png" alt="Example" width="300">

Eventually, I figured it out:

<img src="REPORT.assets/Screen%20Shot%202020-08-01%20at%206.04.46%20PM.png" alt="Example" width="600">

#### Final result

The colors were affected quite a bit by the compression. The yellows have turned to greenish yellows. I wonder why.

There are 3 compression levels: 10%, 50% and 90%. The 10% compression curiously affects the colors more than the 50% and 90% compression, making the colors more bland.:

| 10%                                                          | 50%                                                          | 90%                                                          |
| ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| ![Screen Shot 2020-08-02 at 9.02.09 AM](REPORT.assets/Screen%20Shot%202020-08-02%20at%209.02.09%20AM.png) | ![Screen Shot 2020-08-02 at 9.02.34 AM](REPORT.assets/Screen%20Shot%202020-08-02%20at%209.02.34%20AM.png) | ![Screen Shot 2020-08-02 at 9.02.58 AM](REPORT.assets/Screen%20Shot%202020-08-02%20at%209.02.58%20AM.png) |

The above issue was due to the fact that the dequantization was using the 90% matrix all the time. By using the same dequantization matrix as the quantization one, the below results were obtained. The differences are more difficult to see but are there. This is too bad as I thought the 50% quality from above was much better. I wonder if I have a bug somewhere. The good thing is that the 10-90 range below is a lot more consistent compared to above, telling me that it is actually probably more correct.

| 10%                                                          | 50%                                                          | 90%                                                          |
| ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| ![Screen Shot 2020-08-02 at 9.39.54 AM](REPORT.assets/Screen%20Shot%202020-08-02%20at%209.39.54%20AM.png) | ![Screen Shot 2020-08-02 at 9.39.26 AM](REPORT.assets/Screen%20Shot%202020-08-02%20at%209.39.26%20AM.png) | ![Screen Shot 2020-08-02 at 9.38.51 AM](REPORT.assets/Screen%20Shot%202020-08-02%20at%209.38.51%20AM.png) |

<img src="REPORT.assets/Screen%20Shot%202020-08-02%20at%209.38.51%20AM-6386433.png" alt="Example" width="600">

I did also get the below image in my program. While it looks more correct, the logic behind did not make sense to me.

<img src="REPORT.assets/Screen%20Shot%202020-08-02%20at%209.02.34%20AM.png" alt="Example" width="600">



#### Bugs

The below image is a JPEG compressed with Preview on MacOS, using the lowest setting. This is indicative of a likely bug. The colors match the original image, and the resolution is much higher than with my compressor.

* I think the bug is not in the quantization. I am doing that part correctly. It is therefore upstream. I think it may be the DCT because the pixel values are all being shifted.

<img src="REPORT.assets/Screen%20Shot%202020-08-02%20at%2010.34.29%20AM.png" alt="Example" width="600">

I was hunting for my bug for a couple of hours and I finally found where the bug (just an hour before the assignment was due). My DCT implementation is buggy. I have replaced it with the scipy DCT implementation for now. Since I am submitting this assignment (improved) as my final project, I will reimplement it then. I also left a log where I print a pixel before DCT, and after inverse DCT. They use to be vastly different, which led me to investigate my DCT implementation. They are now very close using scipy's DCT. The below image is after the DCT component was replaced with scipy's.

<img src="REPORT.assets/Screen%20Shot%202020-08-03%20at%204.05.15%20PM-6495984.png" alt="Example" width="600">

In conclusion, the 90% quality from my implementation of JPEG looks really good. My format is compared below to an actual JPEG produced by imagemagick at 50% quality.

| Image    | Compression Time | Decompression Time | Compression Ratio | PSNR with my JPEG | PSNR    |
| -------- | ---------------- | ------------------ | ----------------- | ----------------- | ------- |
| Fall     | 17.1s            | 2.34s              | 2.9               | 11.27dB           | 28.86dB |
| Earth    | 9.0s             | 1.64s              | 4.07              | 11.64dB           | 33.53dB |
| Nature_2 | 14.72s           | 3.02s              | 2.45              | 9.24dB            | 30.03dB |
| Nature   | 8.03s            | 1.0s               | 3.26              | 15.1dB            | 31.30dB |
| Bios     | 13.0s            | 2.25s              | 4.26              | 9.45dB            | 30.85dB |

I wonder why the PSNR values from my image and the JPEG are so different. It appears that my JPEG is of lower quality. Perhaps it is using different quantization tables than mine. 

The most intensive part of my algorithm is the compression as it takes the longest time.

## References

* [Comparative data compression techniques and multi-compression results](https://iopscience.iop.org/article/10.1088/1757-899X/53/1/012081/pdf)
* [Cornell University: JPEG](http://pi.math.cornell.edu/~web6140/TopTenAlgorithms/JPEG.html)
* [The JPEG image code format](https://www.massey.ac.nz/~mjjohnso/notes/59731/presentations/jpeg.pdf)
* [Wikipedia JPEG](https://en.wikipedia.org/wiki/JPEG#Encoding)
* [UC Davies](https://www.ece.ucdavis.edu/cerl/reliablejpeg/compression/)