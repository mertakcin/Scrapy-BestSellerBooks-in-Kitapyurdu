import scrapy


class BooksSpider(scrapy.Spider):
    name = "books"
    page_count = 0
    file = open("bookInfo.txt","a",encoding = 'utf-8')
    book_count = 1
    start_urls = [
        "https://www.kitapyurdu.com/index.php?route=product/best_sellers&list_id=1&filter_in_stock=1&filter_in_stock=1&page=1"
    ]

    def parse(self, response):
        book_names = response.css("div.name.ellipsis a span::text").extract()
        book_authors = response.css("div.author.compact.ellipsis a::text").extract()
        book_publishers = response.css("div.publisher span a span::text").extract()

        i = 0

        while ( i < len(book_names)):

            self.file.write("--------------------------------------\n")
            self.file.write(str(self.book_count) + "." + "\n")
            self.file.write("Kitap İsmi: " + book_names[i] + "\n")
            self.file.write("Yazar: " + book_authors[i] + "\n")
            self.file.write("Publisher: " + book_publishers[i] + "\n")
            self.file.write("--------------------------------------\n")
            self.book_count += 1
            
            i += 1

        next_url = response.css("a.next::attr(href)").extract_first()
        self.page_count += 1

        if next_url is not None and self.page_count != 3:

            yield scrapy.Request(url = next_url, callback = self.parse)

        else:
            self.file.close()

