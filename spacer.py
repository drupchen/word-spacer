from pathlib import Path

from pybo import BoPipeline

from textunits import sentencify


def add_affixed_marker(tokens):
    MARK = '–'
    sent_str = ''
    for t in tokens:
        if t.affix:
            sent_str += ' ' + MARK + t.content
        else:
            sent_str += ' ' + t.content

    return sent_str


def join_affixed_particles(tokens):
    sent_str = ''
    for t in tokens:
        if t.affix:
            sent_str += '' + t.content
        else:
            sent_str += ' ' + t.content

    return sent_str


def format_output(sentences):
    mode = 'join'
    output = []
    for sent in sentences:
        if mode == 'join':
            sent_str = join_affixed_particles(sent[1])
        elif mode == 'mark':
            sent_str = add_affixed_marker(sent[1])
        else:
            raise SyntaxError('mode should either be "join" or "mark"')

        output.append((sent[0], sent_str))

    out = '\n'.join([f'{a[0]},{a[1]}' for a in output])
    return out


if __name__ == '__main__':
    pipeline = BoPipeline('dummy',
                          'pybo',
                          ('pybo_sentences', sentencify),
                          format_output,
                          pybo_profile='GMD')

    for f in Path('input').glob('*.txt'):
        pipeline.pipe_file(f, 'output')
