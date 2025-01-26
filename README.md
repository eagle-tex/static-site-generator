[TOC]



# Purpose

# Inline Parser



# Blocks

## Block types

We assume there are 6 types of markdown blocks, which will be the ones supported.

- "code"
- "heading"
- "ordered_list"
- "paragraph"
- "quote"
- "unordered_list"



## API functions

Refer to each function's docstring for more details.

I didn't copy them here to save time, but it could/should be done if needed.



## 

### `markdown_to_blocks(markdown)`

Takes a raw Markdown string (representing a full document) as input and returns a list of "blocks" strings.

Splits the input into distinct blocks and strip any leading or trailing whitespace from each block. Any "empty" block is removed (in case of excessive newlines).

The following example document should be split into **3** blocks.

```markdown
This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
```


Refer to each function's docstring for more details.
> I didn't copy them here to save time, but it could/should be done if needed.

## API functions

### `markdown_to_text`

### ``
### ``
### ``
### ``
### `is_heading`

### `block_to_block_type(block)`

Takes a single block of Markdown text as input and returns the type of block it is.

### `block_to_block_type`
### `code_block_to_html_node`
### `heading_block_to_html_node`
### `list_to_html_node`
### `ordered_list_to_html_node`
### `unordered_list_to_html_node`
### `paragraph_node_to_html_node(block, "paragraph")`

Convert a Markdown paragraph block into a `ParentNode`

```html
<p>
  This is a paragraph
  Spanning on two lines.
</p>
```



### `quote_block_to_html_node(block, "quote")`

Convert a Markdown quote block into a **blockquote** `ParentNode`

```html
<blockquote>
    <p>Quote 1</p>
    <p>Quote 2</p>
</blockquote>

```



### `parse_markdown`
### `markdown_to_html_node(markdown)`

Uses the other functions to convert a full Markdown document into an `HTMLNode`, specifically a `ParentNode`. The top level element is a `<div>` where each child is a block of the document.

### `paragraph_node_to_html_node`
### `quote_block_to_html_node`
### `parse_markdown`
### `markdown_to_html_node`



## Helper functions
### `stack_repr`
### `clean_stack`
### `add_to_parent`




## Tests

### Class `TestMarkdownToBlocks`: Test `markdown_to_blocks` function
### Class `TestMarkdownToText`: Test `markdown_to_text` function

#### `test_empty_string`

Input: _empty string_
```markdown
""
```

Output: _empty array_

```text
[]
```



#### `test_simple_markdown`

Input: _Markdown text with 3 blocks_

```markdown
# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is a list item
* This is another list item
```

Output: _an array of 3 elements_

```text
[
	"# This is a heading",
	"This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
	"* This is a list item\n* This is another list item",
]
```



#### `test_markdown_with_multiple_blank_lines`

Input: _Markdown with 3 blocks, multiple spaces between blocks and some lines have leading and/or trailing spaces_

```markdown
# This is a heading       
## This is a sub-heading


         This is a paragraph of text.  
    It has some **bold** and *italic* words inside of it.   
      

* This is a list item
    * This is second list item    
        
```

Output: _an array of 3 elements_

```text
[
	"# This is a heading\n## This is a sub-heading",
	"This is a paragraph of text.\nIt has some **bold** and *italic* words inside of it.",
	"* This is a list item\n    * This is second list item",
]
```



### Class `TestBlockToBlock`: Test `block_to_block_type` function

#### `test_block_type_one_of_each`

Input: _An array of 6 blocks (multi-line strings), each block of one type (different types)_

```text
[
	"# Heading\n## Sub-heading",
 	">a quote block\n>second quote\n>third quote",
	"* element 1\n* element 2\n* element 3",
	"```py\nprint('hello')\n```",
	"1. element 1\n2. element 2\n3. element 3",
	"this is a paragraph\nof text",
]
```

Output: _An array of 6 strings, each one being the block type of the corresponding block_

```text
["heading", "quote", "unordered_list", "code", "ordered_list", "paragraph"]
```



#### `test_block_type_all_paragraphs`

Input: _An array of 6 blocks of incorrect Markdown_

```text
[
	"#Heading\n## Sub-heading",  # wrong syntax on '#Heading'
	">a quote block\n >second quote\n>third quote",  # wrong quote syntax on 'second quote'
	"*element 1\n* element 2\n* element 3",  # wrong unordered list syntax on 1 element
	"```py\nprint('hello')\n``",  # code block not closed properly: 2 back ticks instead of 3
	"1. element 1\n2. element 2\n element 3",  # wrong ordered list syntax: jump from 2 to 4
]
```

Output: _An array of 6 strings, all paragraphs, because bad Markdown syntax is just a paragraph_

```text
["paragraph", "paragraph", "paragraph", "paragraph", "paragraph"]
```



#### `test_block_empty_string_raises`

Input: _An empty string_

```markdown
""
```

Output: _No output. The call of `block_to_block_type` raises an Exception_



==CONTINUE HERE==

### Class `TestMarkdownToHtml`: Test `markdown_to_html` function

#### `test_simple_paragraph`

Input: _A simple paragraph (Markdown)_

```markdown
This is a simple paragraph.
```

Output: _The following HTML_

```html
<div>
  <p>This is a simple paragraph.</p>
</div>
```



#### `test_multiple_paragraphs`

Input: _Multiple paragraphs (Markdown)_

```markdown
This is the first paragraph.

This is the second paragraph.
```

Output: _The following HTML_

```html
<div>
  <p>This is the first paragraph.</p>
  <p>This is the second paragraph.</p>
</div>
```



#### `test_headings`

Input: _Headings (Markdown)_

```markdown
# Heading 1
## Heading 2
### Heading 3
```

Output: _The following HTML_

```html
<div>
  <h1>Heading 1</h1>
  <h2>Heading 2</h2>
  <h3>Heading 3</h3>
</div>
```



#### `test_unordered_list`

Input: _Unordered list (Markdown)_

```markdown
- Item 1
- Item 2
 - Item 2.1
 - Item 2.2
```

Output: _The following HTML_

```html
<div>
  <ul>
    <li>Item 1</li>
    <li>Item 2
      <ul>
        <li>Item 2.1</li>
        <li>Item 2.2</li>
      </ul>
    </li>
  </ul>
</div>
```



#### `test_ordered_list`

Input: _Ordered list (Markdown)_

```markdown
1. First
2. Second
 3. Second.1
 4. Second.2
```

Output: _The following HTML_

```html
<div>
  <ol>
    <li>First</li>
    <li>Second
      <ol>
        <li>Second.1</li>
        <li>Second.2</li>
      </ol>
    </li>
  </ol>
</div>
```



#### `test_mixed_lists_one`

Input: _Mixed lists #1 (Markdown)_

```markdown
- Item 1
 1. Subitem 1
 2. Subitem 2
- Item 2
```

Output: _The following HTML_

```html
<div>
  <ul>
    <li>Item 1
      <ol>
        <li>Subitem 1</li>
        <li>Subitem 2</li>
      </ol>
    </li>
    <li>Item 2</li>
  </ul>
</div>
```



#### `test_mixed_lists_two`

Input: _Mixed lists #2 (Markdown)_

```markdown
1. item 1 ordered
2. item 2 ordered
  + item 2.1 unordered
  + item 2.2 unordered
    1. item 2.2.1 ordered
    2. item 2.2.2 ordered
  * item 2.3 unordered
  - item 2.4 unordered
    1. item 2.4.1 ordered
    2. item 2.4.2 ordered
      - item 2.4.2.1 unordered
      * item 2.4.2.2 unordered
3. item 3 ordered
```

Output: _The following HTML_

```html
<div>
  <ol>
    <li>item 1 ordered</li>
    <li>item 2 ordered
      <ul>
        <li>item 2.1 unordered</li>
        <li>item 2.2 unordered
          <ol>
            <li>item 2.2.1 ordered</li>
            <li>item 2.2.2 ordered</li>
          </ol>
        </li>
        <li>item 2.3 unordered</li>
        <li>item 2.4 unordered
          <ol>
            <li>item 2.4.1 ordered</li>
            <li>item 2.4.2 ordered
              <ul>
                <li>item 2.4.2.1 unordered</li>
                <li>item 2.4.2.2 unordered</li>
              </ul>
            </li>
          </ol>
        </li>
      </ul>
    </li>
    <li>item 3 ordered</li>
  </ol>
</div>
```



#### `test_blockquote`

Input: _Blockquote (Markdown)_

```markdown
> This is a quote
```

Output: _The following HTML_

```html
<div>
  <blockquote>
    <p>This is a quote</p>
  </blockquote>
</div>
```



#### `test_code_block`

Input: _Code block (Markdown)_

````markdown
```python3
def hello_world():
	print("Hello, world!")
```
````

Output: _The following HTML_

```html
<div>
  <pre>
  	<code>
			def hello_world():
    			print("Hello, world!")
		</code>
  </pre>
</div>
```



#### `test_combined_elements`

Input: _Combination of elements (Markdown)_

```markdown
# Heading 1

This is a paragraph.

- Item 1
- Item 2

> This is a quote

1. First item
2. Second item
```

Output: _The following HTML_

```html
<div>
  <h1>Heading 1</h1>
  <p>This is a paragraph.</p>
  <ul>
    <li>Item 1</li>
    <li>Item 2</li>
  </ul>
  <blockquote>
    <p>This is a quote</p>
  </blockquote>
  <ol>
    <li>First item</li>
    <li>Second item</li>
  </ol>
</div>
```



#### `test_nested_code_bock_in_list`

Input: _List with code block inside (Markdown)_

```markdown
- Item 1
 - Subitem with code:
    ```
    def nested_code():
        pass
    ```
- Item 2
```

Output: _The following HTML_

```html
<div>
  <ul>
    <li>Item 1
      <ul>
        <li>Subitem with code:
          <pre><code>def nested_code():
    pass</code></pre>
        </li>
      </ul>
    </li>
    <li>Item 2</li>
  </ul>
</div>
```



#### `test_mixed_nested_lists`

Input: _Mixed nesting levels (Markdown)_

```markdown
1. Ordered item 1
   - Unordered subitem 1
   - Unordered subitem 2
      1. Nested ordered subitem 1
      2. Nested ordered subitem 2
         - Nested unordered sub-subitem
2. Ordered item 2
```

Output: _The following HTML_

```html
<div>
  <ol>
    <li>Ordered item 1
      <ul>
        <li>Unordered subitem 1</li>
        <li>Unordered subitem 2
          <ol>
            <li>Nested ordered subitem 1</li>
            <li>Nested ordered subitem 2
              <ul>
                <li>Nested unordered sub-subitem</li>
              </ul>
            </li>
          </ol>
        </li>
      </ul>
    </li>
    <li>Ordered item 2</li>
  </ol>
</div>
```



#### `test_paragraph_and_list`

Input: _Paragraph and list (Markdown)_

```markdown
This is a leading paragraph.

- List item 1
  - Nested list item 1.1
  - Nested list item 1.2

This is a trailing paragraph.
```

Output: _The following HTML_

```html
<div>
  <p>This is a leading paragraph.</p>
  <ul>
    <li>List item 1
      <ul>
        <li>Nested list item 1.1</li>
        <li>Nested list item 1.2</li>
      </ul>
    </li>
  </ul>
  <p>This is a trailing paragraph.</p>
</div>
```



#### `test_blockquote_and_list`

Input: _Blockquote and list (Markdown)_

```markdown
> This is a blockquote

- List item
```

Output: _The following HTML_

```html
<div>
  <blockquote>
    <p>This is a blockquote</p>
  </blockquote>
  <ul>
    <li>List item</li>
  </ul>
</div>
```



#### `test_multiple_blockquotes`

Input: _Multiple blockquotes (Markdown)_

```markdown
> Quote 1

> Quote 2
```

Output: _description_

```html
<div>
  <blockquote>
    <p>Quote 1</p>
  </blockquote>
  <blockquote>
    <p>Quote 2</p>
  </blockquote>
</div>
```



#### `test_mixed_paragraphs_and_headings`

Input: _Mixed paragraphs and headings (Markdown)_

```markdown
# Heading 1

This is a paragraph under heading 1.

## Heading 2

This is a paragraph under heading 2.
```

Output: _The following HTML_

```html
<div>
  <h1>Heading 1</h1>
  <p>This is a paragraph under heading 1.</p>
  <h2>Heading 2</h2>
  <p>This is a paragraph under heading 2.</p>
</div>
```



#### `test_multiple_nested_lists`

Input: _Multiple nested lists (Markdown)_

```markdown
- Level 1
  - Level 2
    - Level 3
- Level 1 again
  - Level 2 again
    - Level 3 again
```

Output: _The following HTML_

```html
<div>
  <ul>
    <li>Level 1
      <ul>
        <li>Level 2
          <ul>
            <li>Level 3</li>
          </ul>
        </li>
      </ul>
    </li>
    <li>Level 1 again
      <ul>
        <li>Level 2 again
          <ul>
            <li>Level 3 again</li>
          </ul>
        </li>
      </ul>
    </li>
  </ul>
</div>
```

















#### `function_name`

Input: _description_

```markdown
"    "
```

Output: _description_

```text
[]
```



#### `function_name`

Input: _description_

```markdown
"    "
```

Output: _description_

```text
[]
```



#### `function_name`

Input: _description_

```markdown
"    "
```

Output: _description_

```text
[]
```



#### `function_name`

Input: _description_

```markdown
"    "
```

Output: _description_

```text
[]
```



#### `function_name`

Input: _description_

```markdown
"    "
```

Output: _description_

```text
[]
```



#### `function_name`

Input: _description_

```markdown
"    "
```

Output: _description_

```text
[]
```



#### `function_name`

Input: _description_

```markdown
"    "
```

Output: _description_

```text
[]
```



#### `function_name`

Input: _description_

```markdown
"    "
```

Output: _description_

```text
[]
```



#### `function_name`

Input: _description_

```markdown
"    "
```

Output: _description_

```text
[]
```



#### `function_name`

Input: _description_

```markdown
"    "
```

Output: _description_

```text
[]
```



#### `function_name`

Input: _description_

```markdown
"    "
```

Output: _description_

```text
[]
```



#### `function_name`

Input: _description_

```markdown
"    "
```

Output: _description_

```text
[]
```



#### `function_name`

Input: _description_

```markdown
"    "
```

Output: _description_

```text
[]
```



#### `function_name`

Input: _description_

```markdown
"    "
```

Output: _description_

```text
[]
```



#### `function_name`

Input: _description_

```markdown
"    "
```

Output: _description_

```text
[]
```



#### `function_name`

Input: _description_

```markdown
"    "
```

Output: _description_

```text
[]
```



#### `function_name`

Input: _description_

```markdown
"    "
```

Output: _description_

```text
[]
```



#### `function_name`

Input: _description_

```markdown
"    "
```

Output: _description_

```text
[]
```



#### `function_name`

Input: _description_

```markdown
"    "
```

Output: _description_

```text
[]
```



#### `function_name`

Input: _description_

```markdown
"    "
```

Output: _description_

```text
[]
```



#### `function_name`

Input: _description_

```markdown
"    "
```

Output: _description_

```text
[]
```



#### `function_name`

Input: _description_

```markdown
"    "
```

Output: _description_

```text
[]
```



#### `function_name`

Input: _description_

```markdown
"    "
```

Output: _description_

```text
[]
```



#### `function_name`

Input: _description_

```markdown
"    "
```

Output: _description_

```text
[]
```



#### `function_name`

Input: _description_

```markdown
"    "
```

Output: _description_

```text
[]
```



#### `function_name`

Input: _description_

```markdown
"    "
```

Output: _description_

```text
[]
```



#### `function_name`

Input: _description_

```markdown
"    "
```

Output: _description_

```text
[]
```



#### `function_name`

Input: _description_

```markdown
"    "
```

Output: _description_

```text
[]
```



#### `function_name`

Input: _description_

```markdown
"    "
```

Output: _description_

```text
[]
```



#### `function_name`

Input: _description_

```markdown
"    "
```

Output: _description_

```text
[]
```



#### `function_name`

Input: _description_

```markdown
"    "
```

Output: _description_

```text
[]
```



#### `function_name`

Input: _description_

```markdown
"    "
```

Output: _description_

```text
[]
```



#### `function_name`

Input: _description_

```markdown
"    "
```

Output: _description_

```text
[]
```



#### `function_name`

Input: _description_

```markdown
"    "
```

Output: _description_

```text
[]
```



#### `function_name`

Input: _description_

```markdown
"    "
```

Output: _description_

```text
[]
```



#### `function_name`

Input: _description_

```markdown
"    "
```

Output: _description_

```text
[]
```



#### `function_name`

Input: _description_

```markdown
"    "
```

Output: _description_

```text
[]
```



#### `function_name`

Input: _description_

```markdown
"    "
```

Output: _description_

```text
[]
```



#### `function_name`

Input: _description_

```markdown
"    "
```

Output: _description_

```text
[]
```



#### `function_name`

Input: _description_

```markdown
"    "
```

Output: _description_

```text
[]
```



#### `function_name`

Input: _description_

```markdown
"    "
```

Output: _description_

```text
[]
```



#### `function_name`

Input: _description_

```markdown
"    "
```

Output: _description_

```text
[]
```



#### `function_name`

Input: _description_

```markdown
"    "
```

Output: _description_

```text
[]
```









### 


# Website



