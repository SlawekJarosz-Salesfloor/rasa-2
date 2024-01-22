import Pmw
import traceback

from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox 

from CLASS_Tagging_Workflow import *
from CLASS_Nlu_Workflow import *

# from optimized_nlu_server import getRegExMatch, get_mapping_and_prefix
class DoubleScrolledFrame:
    """
    A vertically scrolled Frame that can be treated like any other Frame
    ie it needs a master and layout and it can be a master.
    keyword arguments are passed to the underlying Frame
    except the keyword arguments 'width' and 'height', which
    are passed to the underlying Canvas
    note that a widget layed out in this frame will have Canvas as self.master,
    if you subclass this there is no built in way for the children to access it.
    You need to provide the controller separately.
    """
    def __init__(self, master, **kwargs):
        # Initialize the DoubleScrolledFrame class.
        width = kwargs.pop('width', None)
        height = kwargs.pop('height', None)
        self.outer = tk.Frame(master, **kwargs)

        self.vsb = ttk.Scrollbar(self.outer, orient=tk.VERTICAL)
        self.vsb.grid(row=0, column=1, sticky='ns')
        self.hsb = ttk.Scrollbar(self.outer, orient=tk.HORIZONTAL)
        self.hsb.grid(row=1, column=0, sticky='ew')
        self.canvas = tk.Canvas(self.outer, highlightthickness=0, width=width, height=height)
        self.canvas.grid(row=0, column=0, sticky='nsew')
        self.outer.rowconfigure(0, weight=1)
        self.outer.columnconfigure(0, weight=1)
        self.canvas['yscrollcommand'] = self.vsb.set
        self.canvas['xscrollcommand'] = self.hsb.set
        # mouse scroll does not seem to work with just "bind"; You have
        # to use "bind_all". Therefore to use multiple windows you have
        # to bind_all in the current widget
        self.canvas.bind("<Enter>", self._bind_mouse)
        self.canvas.bind("<Leave>", self._unbind_mouse)
        self.vsb['command'] = self.canvas.yview
        self.hsb['command'] = self.canvas.xview

        self.inner = tk.Frame(self.canvas)
        # pack the inner Frame into the Canvas with the topleft corner 4 pixels offset
        self.canvas.create_window(4, 4, window=self.inner, anchor='nw')
        self.inner.bind("<Configure>", self._on_frame_configure)

        self.outer_attr = set(dir(tk.Widget))

    def __getattr__(self, item):
        if item in self.outer_attr:
            # geometry attributes etc (eg pack, destroy, tkraise) are passed on to self.outer
            return getattr(self.outer, item)
        else:
            # all other attributes (_w, children, etc) are passed to self.inner
            return getattr(self.inner, item)

    def _on_frame_configure(self, event=None):
        x1, y1, x2, y2 = self.canvas.bbox("all")  # pyright: ignore[reportUnusedVariable]
        height = self.canvas.winfo_height()
        width = self.canvas.winfo_width()
        self.canvas.config(scrollregion=(0, 0, max(x2, width), max(y2, height)))

    def _bind_mouse(self, event=None):
        self.canvas.bind_all("<4>", self._on_mousewheel)
        self.canvas.bind_all("<5>", self._on_mousewheel)
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _unbind_mouse(self, event=None):
        self.canvas.unbind_all("<4>")
        self.canvas.unbind_all("<5>")
        self.canvas.unbind_all("<MouseWheel>")

    def _on_mousewheel(self, event):
        """Linux uses event.num; Windows / Mac uses event.delta"""
        func = self.canvas.xview_scroll if event.state & 1 else self.canvas.yview_scroll
        if event.num == 4 or event.delta > 0:
            func(-1, "units")
        elif event.num == 5 or event.delta < 0:
            func(1, "units")

    def __str__(self):
        return str(self.outer)

FLASHING_PERIOD = 500 # ms

class FlashingLabel(tk.Label):
    
    def __init__(self, parent, *args, **kwargs):
        Label.__init__(self, parent, *args, **kwargs)   # <-- pass parent parameter
        self.is_running = False
        self.original_background = self.cget("background")
        self.original_foreground = self.cget("foreground")
        # self.flash()

    def start(self):
        self.is_running = True

    def stop(self):
        self.is_running = False
        self.config(background=self.original_background, foreground=self.original_foreground)

    def error(self):
        self.is_running = False
        self.config(background=self.original_background, foreground='red')

    def flash(self):
        bg = self.cget("background")
        fg = self.cget("foreground")
        self.config(background=fg, foreground=bg)
        # self.after(FLASHING_PERIOD, self.flash)

import threading
def task_thread(task_function_name):
  task_thread = threading.Thread(target=task_function_name)
  task_thread.start()
  return task_thread

def get_product_categories():
    product_categories = []
    for category in select_db_names:
        if select_db_states[category].get() == 1:
            product_categories.append(category)

    return product_categories

def run_tagging_workflow():
    product_categories = get_product_categories()
    if len(product_categories) == 0:
        messagebox.showwarning(title='No Category', message='Have to select at least 1 category.')
        return

    category_state = {}    
    for category in product_categories:
        category_state[category] = ''
        label_db_names[category].flash()
        tagging_workflow = Production_Workflow(category) # pyright: ignore[reportUnusedVariable] 
        for step in select_step_states:
            if select_step_states[step].get() == 1:
                print()
                printInfo(f'Running {step}')
                select_step_labels[step].flash()
                window.update()
                parameter = ''
                try:
                    if step == 'Migrate Data':
                        from tkinter import simpledialog
                        answer = ''
                        while answer == '':
                            answer = simpledialog.askstring(
                                "Source Database", "What is the source db name?",
                                initialvalue=f"Saks-{category}", parent=window)
                            if answer == None:
                                messagebox.showwarning(title='Source Database', message='Have to specify db name to migrate data from.')
                                return
                        parameter = answer
                    if parameter == '':
                        eval(f'tagging_workflow.{tagging_steps[step]}()')
                    else:
                        eval(f'tagging_workflow.{tagging_steps[step]}("{parameter}")')
                except:
                    traceback.print_exc()
                    select_step_labels[step].error()
                    return
                select_step_labels[step].stop()
                category_state[category] = step
        label_db_names[category].stop()

    json.dump(category_state, open('./prep/_tagging_state.json', 'w'), indent=4)

    printInfo('Finished tagging workflow')
    messagebox.showinfo(message='NLU workflow completed successfully')

def run_nlu_workflow():
    product_categories = get_product_categories()
    if len(product_categories) == 0:
        messagebox.showwarning(title='No Category', message='Have to select at least 1 category.')
        return
    nlu_workflow = Nlu_Workflow(product_categories) # pyright: ignore[reportUnusedVariable] 
    for step in nlu_step_states:
        if nlu_step_states[step].get() == 1:
            print()
            printInfo(f'Running {step}')
            nlu_step_labels[step].flash()
            window.update()
            window.update()
            try:
                eval(f'nlu_workflow.{nlu_steps[step]}()')
            except:
                traceback.print_exc()
                nlu_step_labels[step].error()
                return
            nlu_step_labels[step].stop()

    printInfo('Finished NLU workflow')
    messagebox.showinfo(message='NLU workflow completed successfully')

def clean_up(db_type=None):
    product_categories = get_product_categories()
    if len(product_categories) == 0:
        messagebox.showwarning(title='No Category', message='Have to select at least 1 category.')
        return
    
    for category in product_categories:
        tagging_workflow = Production_Workflow(category)
        tagging_workflow.product_db.set_db_name(db_type)
        answer = messagebox.askokcancel('Delete Database', f'Do you really want to delete {tagging_workflow.product_db.db_name}?')
        if answer:
            tagging_workflow.delete_db(db_type)

def search_db(__=None):
    def show_wide_display(results):
        top_level = Toplevel(height=400, width=500)
        result_frame = DoubleScrolledFrame(top_level,height=400, width=600)
        result_frame.pack(fill='both', expand=True)
        result_text = Text(result_frame)
        result_text.pack(fill='both', expand=True)
        # Insert the results
        result_text.insert(tk.END, results)
        top_level.update()

    product_categories = get_product_categories()
    if len(product_categories) == 0:
        messagebox.showwarning(title='No Category', message='Have to select at least 1 category.')
        return
    
    if len(search_word.get()) == 0:
        return
    
    nlu_workflow = Nlu_Workflow(product_categories) # pyright: ignore[reportUnusedVariable]
    products_found = nlu_workflow.search_dbs(search_word.get())
    show_wide_display('\n'.join(products_found))

product_categories = ['CoatsJackets', 'Dresses', 'Jeans',
                      'Jumpsuits', 'Pants', 'Shorts', 'Skirts', 'Sleepwear',
                      'Sweaters', 'SweatshirtsHoodies', 'Tops']    
window = Tk()
window.bind('<Return>', search_db)
window.title("Tagging and NLU creation")
Pmw.initialise(window)
# Add content to the left frame
current_row = 0
main_frame = DoubleScrolledFrame(window, width=930, height=690)    
main_frame.grid(row=0, column=0, sticky=NSEW, padx=5, pady=5)

product_title_label = ttk.Label(main_frame, width=20, text='PRODUCT CATEGORIES', font='Helvetica 18 bold')
product_title_label.grid(column=0, row=current_row)
balloon = Pmw.Balloon(window)
status_colours = {'orange':'Ready for LLM tagging','purple':'LLM tagged','blue':'NLU output validated','green':'Rasa tagged + fixed'}
balloon.bind(product_title_label, 'Status Legend:\nyellow = Ready for LLM tagging\npurple = LLM tagged\nblue = NLU output validated\ngreen = Rasa tagged + fixed')

title_steps_label = FlashingLabel(main_frame, width=20, text='TAGGING STEPS', font='Helvetica 18 bold')
title_steps_label.grid(column=1, row=current_row)
ttk.Label(main_frame, width=10, text='CLEAN UP', font='Helvetica 18 bold').grid(column=2, row=current_row)

current_row += 1

status_frame = Frame(main_frame, width=400, relief=RAISED, borderwidth=1)
status_frame.grid(row=current_row, column=0, sticky=E, padx=5, pady=5)

legend_frame = Frame(status_frame, width=400, relief=RAISED, borderwidth=1)
legend_frame.grid(row=0, column=0, sticky=EW, padx=5, pady=5)
ttk.Label(legend_frame, width=20, text='Legend', font='Helvetica 16 bold').grid(column=0, row=0)
for idx, colour in enumerate(status_colours):
    FlashingLabel(legend_frame, width=25, text=status_colours[colour], background=colour).grid(column=0, row=idx + 1, sticky=W, padx=5, pady=2)

db_name_frame = Frame(status_frame, width=400, relief=RAISED, borderwidth=1)
db_name_frame.grid(row=1, column=0, sticky=EW, padx=5, pady=5)
label_db_names = {}
select_db_names = {}
select_db_states = {}
ready_state = json.load(open('./prep/_ready_state.json'))
for idx, category in enumerate(product_categories):
    background_state = window.cget("background")
    if category in ready_state:
        background_state = ready_state[category]
    label_db_names[category] = FlashingLabel(db_name_frame, width=20, text=category, background=background_state)
    label_db_names[category].grid(column=0, row=idx, padx=5, pady=2)
    select_db_states[category] = tk.IntVar()
    select_db_names[category] = ttk.Checkbutton(db_name_frame, width=5, variable=select_db_states[category])
    select_db_names[category].grid(column=1, row=idx, sticky=EW, padx=5, pady=2) 

step_name_frame = Frame(main_frame, width=250, relief=RAISED, borderwidth=1)
step_name_frame.grid(row=current_row, column=1, sticky=NS, padx=5, pady=5)
tagging_steps = {
    'Prep'                           : 'prep_dbs', 
    'Update Ontology'                : 'update_ontology', 
    'Clone Ontology to Products Db'  : 'clone_ontology_to_products_db', 
    'Migrate Data'                   : 'migrate_data', 
    'Get Baseline'                   : 'get_baseline_stats', 
    'Fix Description'                : 'fix_description',
    'ViSenze Mapping'                : 'map_visual_tags', 
    'Clone Products to LLM Db'       : 'clone_products_to_llm_db', 
    'Tag Using LLM'                  : 'tag_llm', 
    'Clone LLM to Fix Db'            : 'clone_llm_to_fix_db', 
    'Fix LLM Tags'                   : 'fix_llm_tags', 
    'Approve Tagged Products'        : 'approve_products', 
    '--- AFTER NLU CREATED ---'      : '',
    'Clone Fix to Rasa Db'           : 'clone_fix_to_rasa_db', 
    'Tag Using Rasa'                 : 'tag_rasa',
    'Fix Rasa Tags'                  : 'fix_rasa_tags', 
    'Validate CLU'                   : 'validate_clu',
    'Check consistency'              : 'check_consistency',

    #  "TEST ONLY": 'TEST_FUNCTION'
    # 'Fix URIs'                       : 'fix_uris',
    }

select_step_labels = {}
select_step_names  = {}
select_step_states = {}
for idx, step in enumerate(tagging_steps):
    select_step_labels[step] = FlashingLabel(step_name_frame, width=25, text=step)
    select_step_labels[step].grid(column=0, row=idx, padx=5, pady=2)
    select_step_states[step] = tk.IntVar()
    if tagging_steps[step] == '':
        continue
    select_step_names[step] = ttk.Checkbutton(step_name_frame, width=5, variable=select_step_states[step])
    select_step_names[step].grid(column=1, row=idx, sticky=EW, padx=5, pady=2)

ttk.Button(step_name_frame, text= "Start Tagging Workflow", command=run_tagging_workflow).grid(column=0, row=idx+1, columnspan=2, pady=10)


select_step_names['Prep'].config(state=DISABLED)
select_step_states['Prep'].set(1)
select_step_names['Get Baseline'].config(state=DISABLED)
select_step_states['Get Baseline'].set(1)

# Buttons for some common actions
action_frame = Frame(main_frame, width=400, relief=RAISED, borderwidth=1)
action_frame.grid(row=current_row, column=2, sticky=NSEW, padx=5, pady=5)
action_buttons = {}
for prod_step in range(Production_Step.PRODUCTS.value, Production_Step.FINAL.value):
    action_buttons[prod_step] = ttk.Button(action_frame, width=20, 
                                           text='Delete ' + str(Production_Step(prod_step)).split('.')[1] + ' db', 
                                           command=lambda prod_step=prod_step: clean_up(Production_Step(prod_step)))
    action_buttons[prod_step].grid(column=1, row=prod_step, padx=10) 

current_row += 1

# use_cache_var = tk.IntVar()
# Label(main_frame, width=20, text="Use Cache").grid(column=0, row=current_row)
# ttk.Checkbutton(main_frame, width=10, variable=use_cache_var).grid(column=1, row=current_row) 

current_row += 1

nlu_steps = {
            'Check Tag Quality'  : 'check_tag_quality', 
            'Create NLU Training': 'generate_nlu', 
            }
ttk.Label(main_frame, text="NLU - ACROSS ALL PRODUCT CATEGORIES", font='Helvetica 18 bold').grid(column=0, row=current_row, columnspan=2)

current_row += 1

nlu_frame = Frame(main_frame, width=400, relief=RAISED, borderwidth=1)
nlu_frame.grid(row=current_row, column=0, sticky=NSEW, padx=5, pady=10, columnspan=2)

search_frame = Frame(main_frame, width=200, relief=RAISED, borderwidth=1)
search_frame.grid(row=current_row, column=2, sticky=NSEW, padx=5, pady=10)

nlu_step_labels = {}
nlu_step_names  = {}
nlu_step_states = {}
for idx, step in enumerate(nlu_steps):
    nlu_step_labels[step] = FlashingLabel(nlu_frame, width=50, text=step)
    nlu_step_labels[step].grid(column=0, row=idx + 1)
    nlu_step_states[step] = tk.IntVar()
    nlu_step_names[step] = ttk.Checkbutton(nlu_frame, width=20, variable=nlu_step_states[step])
    nlu_step_names[step].grid(column=1, row=idx + 1, sticky=W) 

current_row += idx + 2

ttk.Button(nlu_frame, text= "Generate NLU", command=run_nlu_workflow).grid(column=0, row=current_row, columnspan=2)

search_word   = ttk.Entry(search_frame)
search_word.grid(column=0, row=0, padx=5, pady=5)
search_button = ttk.Button(search_frame, width=20, text='Search', command=search_db)
search_button.grid(column=0, row=1, padx=5, pady=5)

window.grid_columnconfigure(0,weight=1) # the text and entry frames column
window.grid_rowconfigure(0, weight=1) # all frames row

window.mainloop()