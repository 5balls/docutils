# Author: Florian Pesth
# Copyright: This module has been placed in the public domain.

"""
Directive for the creation of navigation elements for a webpage. The
idea is, that just a title for the navigation function of this page
needs to be given. From the placement in the file system and the
navigation elements of the other pages above or on the same directory
level an unordered list in a <nav> element is generated and can be
styled later via css to provide a nice visual menu.
"""

__docformat__ = 'reStructuredText'

import os
import io
import threading
from docutils import nodes, utils
from docutils.parsers.rst import Directive
from docutils.parsers.rst import directives, states
from docutils.nodes import fully_normalize_name, whitespace_normalize_name, bullet_list, list_item, paragraph, reference, target
from docutils.parsers.rst.roles import set_classes
from docutils.nodes import Element
from docutils.core import publish_doctree

class navigation(Element):
    basic_attributes = None
    local_attributes = None
    pass

def is_navigation(node):
    return node.tagname == 'navigation'

class Navigation(Directive):
    has_content = False
    required_arguments = 0
    final_argument_whitespace = True
    old_depth = 1
    call_depth = 0
    option_spec = {'class': directives.class_option,
                   'title': directives.unchanged,
                   'index': directives.unchanged,
                   'base': directives.unchanged,
                   'language': directives.unchanged}

    def run(self):
        Navigation.call_depth = Navigation.call_depth + 1
        node = navigation()
        # Get all titles:
        source_base_dir = os.path.abspath(self.options['base'])
        own_rel_path, own_filename = os.path.split(self.state_machine.document.current_source)
        own_abs_path = os.path.join(os.getcwd(), own_rel_path)
        os.write(2, ("own_abs_path %s\n" % own_abs_path).encode("utf-8"))
        own_nav_dir = os.path.relpath(own_abs_path, source_base_dir)
        os.write(2, ("source_base_dir %s own_nav_dir %s\n" % (source_base_dir, own_nav_dir)).encode("utf-8"))
        cur_bullet_list_node = bullet_list()
        cur_bullet_list_node['bullet'] = '-'
        cur_nav_element = cur_bullet_list_node
        cur_class = None
        nav_elements = [None] * 1000
        nav_elements_indexless = [None] * 1000
        if 'title' in self.options:
            node['title'] = self.options['title']
        else:
            node['title'] = ''
        if 'index' in self.options:
            node['index'] = self.options['index']
        else:
            node['index'] = 0
        if 'class' in self.options:
            node['class'] = self.options['class']
        if 'language' in self.options:
            node['language'] = self.options['language']
        else:
            node['language'] = 'de'

        if Navigation.call_depth > 1:
            os.write(2, ("Skip parsing for recursive calls...\n").encode("utf-8"))
            return [node]

        for dirpath, dirnames, filenames in os.walk(source_base_dir):
            for dirname in dirnames:
                if '.git' in dirname:
                    continue
                cur_path = os.path.join(dirpath, dirname)
                if '.git' in cur_path:
                    continue
                os.write(2, ("%s %s\n" % (cur_path, filenames)).encode("utf-8"))
                self.new_depth = cur_path.count(os.sep)-source_base_dir.count(os.sep)
                if(self.new_depth > self.old_depth):
                    os.write(2, ("+\n").encode("utf-8"))
                    last_nav_element = cur_nav_element
                    if cur_class is not None:
                        cur_bullet_list_node['classes'] = cur_class
                    for nav_element in nav_elements + nav_elements_indexless:
                        if nav_element is not None:
                            cur_bullet_list_node.append(nav_element)
                            last_nav_element = nav_element
                    cur_class = None
                    nav_elements = [None] * 1000
                    nav_elements_indexless = [None] * 1000
                    self.old_depth = self.new_depth
                    cur_bullet_list_node = bullet_list()
                    cur_bullet_list_node['bullet'] = '-'
                    last_nav_element.append(cur_bullet_list_node)

                rel_path = os.path.relpath(cur_path,own_abs_path)
                rel_commonpart = os.path.commonprefix([os.path.split(cur_path)[0],own_abs_path])
                if not (rel_commonpart == os.path.split(cur_path)[0]):
                    continue
                (_,_,real_filenames) = next(os.walk(os.path.join(dirpath, dirname)))
                for filename in real_filenames:
                    if (filename[:-2] + node['language'] in real_filenames and filename[-2:] != node['language']):
                        os.write(2,('nok %i %i %s %s %s %s %s %s\n' % (self.new_depth, self.old_depth, filename[:-2] + node['language'], real_filenames, node['language'], filename[-2:], filename, map(lambda x: x.astext(), list(filter(lambda x: x is not None, nav_elements))))).encode("utf-8"))
                        continue
                    os.write(2,('%i ok %i %i %s %s %s %s %s %s\n' % (Navigation.call_depth, self.new_depth, self.old_depth, filename[:-2] + node['language'], real_filenames, node['language'], filename[-2:], filename, map(lambda x: x.astext(), list(filter(lambda x: x is not None, nav_elements))))).encode("utf-8"))
                    cur_file = io.open(os.path.join(dirpath, dirname, filename), mode='r', encoding='utf-8')
                    cur_file_rst_content = cur_file.read()
                    cur_file_doc_tree = publish_doctree(cur_file_rst_content, settings_overrides={'input_encoding': 'unicode'})
                    cur_file.close()
                    nav_elements_doc = cur_file_doc_tree.traverse(condition=is_navigation)
                    if not nav_elements_doc:
                        continue
                    cur_nav_element = nav_elements_doc[0]
                    cur_title = cur_nav_element['title']
                    cur_index = int(cur_nav_element['index'])
                    if 'class' in cur_nav_element:
                        cur_class = cur_nav_element['class']
                    cur_nav_element = list_item()
                    cur_nav_element_paragraph = paragraph();

                    if os.path.commonprefix([cur_path,own_abs_path]) == cur_path:
                        cur_nav_element_paragraph['classes'] = ['navigation-selected']
                    cur_nav_element_paragraph_reference = reference(text=cur_title)
                    cur_nav_element_paragraph_reference['name'] = cur_title
                    cur_nav_element_paragraph_reference['refuri'] = rel_path
                    cur_nav_element_paragraph.append(cur_nav_element_paragraph_reference)
                    cur_nav_element.append(cur_nav_element_paragraph)
                    if(cur_index != 0):
                        nav_elements[cur_index] = cur_nav_element
                    else:
                        nav_elements_indexless.append(cur_nav_element)

        for nav_element in nav_elements + nav_elements_indexless:
            if nav_element is not None:
                cur_bullet_list_node.append(nav_element)

        if cur_class is not None:
            cur_bullet_list_node['classes'] = cur_class
        Navigation.call_depth = Navigation.call_depth - 1
        node.append(cur_bullet_list_node)
        return [node]
