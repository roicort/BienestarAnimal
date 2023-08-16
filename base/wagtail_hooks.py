from wagtail import hooks

#List of all items in menu
    #fragmentos
    #documents
    #images
    #explorer
    #propiedades
    #informes

@hooks.register('construct_main_menu')
def hide_explorer_menu(request, menu_items):
    for item in menu_items:
        print(item.nombre)
    menu_items[:] = [item for item in menu_items if (item.nombre == 'fragmentos')]