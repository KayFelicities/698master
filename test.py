#coding=utf-8  


def del_brackets(str_text, match_text='()'):
    """del brackets"""
    match_text = match_text.strip()
    left = match_text[0]
    right = match_text[1]

    ret_text = str_text
    while True:
        left_pos = ret_text.find(left)
        if left_pos >= 0:
            depth = 1
            for count, letter in enumerate(ret_text[left_pos + 1:], 1):
                if letter == left:
                    depth += 1
                if letter == right:
                    depth -= 1
                if depth == 0:
                    ret_text = ret_text[:left_pos] + ret_text[left_pos + count + 1:]
                    break
        else:
            return ret_text

if __name__ == '__main__':
    print(del_brackets('()', 'asb(((jkl)lk)j)o(dfj))lkj'))

