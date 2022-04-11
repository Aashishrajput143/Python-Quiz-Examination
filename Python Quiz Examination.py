#!/usr/bin/env python
# coding: utf-8

# In[1]:


from tkinter import *
from tkinter import messagebox,filedialog,ttk
from tkinter.ttk import Combobox,Treeview,Scrollbar,Style
from PIL import Image,ImageTk
import sqlite3 as sql
import random
from datetime import datetime


# In[37]:


win=Tk()
win.state('zoomed')
win.title('Python Quiz Examination')
win.configure(bg="sky blue")
win.resizable(width=False,height=False)

title=Label(win,text='Python Quiz Examination',font=('Arial',40,'underline','bold'),bg='sky blue')
title.place(relx=.283,rely=.05)

login_img=Image.open("login.png").resize((110,40))
login_imgtk=ImageTk.PhotoImage(login_img)

reset_img=Image.open("reset.png").resize((110,40))
reset_imgtk=ImageTk.PhotoImage(reset_img)

back_img=Image.open("back.png").resize((110,40))
back_imgtk=ImageTk.PhotoImage(back_img)

logout_img=Image.open("logout.png").resize((110,40))
logout_imgtk=ImageTk.PhotoImage(logout_img)

newuser_img=Image.open("newuser.png").resize((260,50))
newuser_imgtk=ImageTk.PhotoImage(newuser_img)

register_img=Image.open("register.png").resize((150,50))
register_imgtk=ImageTk.PhotoImage(register_img)

delete_img=Image.open("delete.png").resize((130,50))
delete_imgtk=ImageTk.PhotoImage(delete_img)

update_img=Image.open("update.png").resize((130,50))
update_imgtk=ImageTk.PhotoImage(update_img)

def login_screen():
    
    frm=Frame(win)
    frm.configure(bg='green')
    frm.place(relx=0,rely=.15,relwidth=1,relheight=1)
    
    def reset(event):
        entry_user.delete(0,"end")
        entry_pass.delete(0,"end")
        type_cb.current(0)
        entry_user.focus()
        
    def newuser(event):
        frm.destroy()
        newuser_screen()
        
    def login(event):
        u=entry_user.get()
        p=entry_pass.get()
        if(len(u)==0 or len(p)==0):
            messagebox.showerror("Validation","Please fill both fields")
        else:
            t=type_cb.get()
            if(t=="USER"):
                con=sql.connect(database="quiz.sqlite")
                cur=con.cursor()
                cur.execute("select * from users where username=? and password=?",(u,p))
                global user
                user=cur.fetchone()
                if(user==None):
                    messagebox.showerror("Validation","Invalid Username/Password")
                else:
                    frm.destroy()
                    user_screen()
            else:
                if(u=='admin' and p=='admin'):
                    messagebox.showinfo("","valid ADMIN")
                    frm.destroy()
                    admin_login()
                else:
                    messagebox.showerror("Validation","Invalid admin")
    
    lbl_user=Label(frm,text="Username:",font=('Arial',20,'bold'),bg='green')
    lbl_user.place(relx=.35,rely=.13)
    
    entry_user=Entry(frm,font=('Arial',20,'bold'),bd=5)
    entry_user.place(relx=.5,rely=.13)
    entry_user.focus()
    
    lbl_pass=Label(frm,text="Password:",font=('Arial',20,'bold'),bg='green')
    lbl_pass.place(relx=.35,rely=.26)
    
    entry_pass=Entry(frm,font=('Arial',20,'bold'),bd=5,show="*")
    entry_pass.place(relx=.5,rely=.26)
    
    lbl_type=Label(frm,text="Type:",font=('Arial',20,'bold'),bg='green')
    lbl_type.place(relx=.35,rely=.39)

    type_cb=Combobox(frm,font=('Arial',20,'bold'),values=['USER','ADMIN'])
    type_cb.current(0)
    type_cb.place(relx=.5,rely=.39)
    
    login_btn=Label(frm,image=login_imgtk,bg='green')
    login_btn.place(relx=.5,rely=.485)
    login_btn.bind("<Button>",login)
    
    reset_btn=Label(frm,image=reset_imgtk,bg='green')
    reset_btn.place(relx=.6,rely=.485)
    reset_btn.bind("<Button>",reset)
    
    reg_btn=Label(frm,image=newuser_imgtk,bg='green')
    reg_btn.place(relx=.5,rely=.57)
    reg_btn.bind("<Button>",newuser)
    
def newuser_screen():
    frm=Frame(win)
    frm.configure(bg='green')
    frm.place(relx=0,rely=.15,relwidth=1,relheight=1)
    
    def back(event):
        frm.destroy()
        login_screen()
    
    def register(event):
        u=entry_user.get()
        p=entry_pass.get()
        if(len(u)==0 or len(p)==0):
            messagebox.showerror("Validation","Please fill both fields")
        else:
            try:
                con=sql.connect(database="quiz.sqlite")
                cur=con.cursor()
                cur.execute("insert into users values(?,?)",(u,p))
                con.commit()
                messagebox.showinfo("Users","Account created")
                frm.destroy()
                login_screen()
            except:
                messagebox.showerror("User","Username already exists!")
            con.close()
        
    lbl_user=Label(frm,text="Username:",font=('Arial',20,'bold'),bg='green')
    lbl_user.place(relx=.35,rely=.13)
    
    entry_user=Entry(frm,font=('Arial',20,'bold'),bd=5)
    entry_user.place(relx=.5,rely=.13)
    entry_user.focus()
    
    lbl_pass=Label(frm,text="Password:",font=('Arial',20,'bold'),bg='green')
    lbl_pass.place(relx=.35,rely=.26)

    entry_pass=Entry(frm,font=('Arial',20,'bold'),bd=5,show="*")
    entry_pass.place(relx=.5,rely=.26)
    
    reg_btn=Label(frm,image=register_imgtk,bg='green')
    reg_btn.place(relx=.6,rely=.375)
    reg_btn.bind("<Button>",register)
    
    back_btn=Label(frm,image=back_imgtk,bg='green')
    back_btn.place(relx=0,rely=0)
    back_btn.bind("<Button>",back)
    
def admin_login():
    frm=Frame(win)
    frm.configure(bg='green')
    frm.place(relx=0,rely=.15,relwidth=1,relheight=.92)
    
    def logout(event):
            option=messagebox.askyesno('confirmation','Do you want to logout?')
            if(option==True):
                frm.destroy()
                login_screen()
    
    def set_questions():
        frm=Frame(win)
        frm.configure(bg='#2B547E')
        frm.place(relx=.21,rely=.15,relwidth=1,relheight=.92)
        
        def logout(event):
            option=messagebox.askyesno('confirmation','Do you want to logout?')
            if(option==True):
                frm.destroy()
                login_screen()
        
        def setques(event):
            ques=question_entry.get()
            op1=opt1_entry.get()
            op2=opt2_entry.get()
            op3=opt3_entry.get()
            op4=opt4_entry.get()
            ans=ans_entry.get()
        
            con=sql.connect(database="quiz.sqlite")
            cur=con.cursor()
            cur.execute("select max(ques_id) from questions")
            qid=cur.fetchone()[0]
            qid+=1
            con.close()
        
            con=sql.connect(database="quiz.sqlite")
            cur=con.cursor()
            cur.execute("insert into questions values(?,?,?,?,?,?,?)",(qid,ques,op1,op2,op3,op4,ans))
            con.commit()
            con.close()
            messagebox.showinfo("Question","Question inserted")
            question_entry.delete(0,"end")
            opt1_entry.delete(0,"end")
            opt2_entry.delete(0,"end")
            opt3_entry.delete(0,"end")
            opt4_entry.delete(0,"end")
            ans_entry.delete(0,"end")
            question_entry.focus()
        
        question_label=Label(frm,text="Question :-",font=('Arial',20,'bold'),bg='#2B547E')
        question_label.place(relx=.2,rely=.1)
        
        question_entry=Entry(frm,font=('Arial',20,'bold'))
        question_entry.place(relx=.35,rely=.1)
        question_entry.focus()
        
        opt1_label=Label(frm,text="Option 1 :-",font=('Arial',20,'bold'),bg='#2B547E')
        opt1_label.place(relx=.2,rely=.2)
        
        opt1_entry=Entry(frm,font=('Arial',20,'bold'))
        opt1_entry.place(relx=.35,rely=.2)
        
        opt2_label=Label(frm,text="Option 2 :-",font=('Arial',20,'bold'),bg='#2B547E')
        opt2_label.place(relx=.2,rely=.3)
        
        opt2_entry=Entry(frm,font=('Arial',20,'bold'))
        opt2_entry.place(relx=.35,rely=.3)
        
        opt3_label=Label(frm,text="Option 3 :-",font=('Arial',20,'bold'),bg='#2B547E')
        opt3_label.place(relx=.2,rely=.4)
        
        opt3_entry=Entry(frm,font=('Arial',20,'bold'))
        opt3_entry.place(relx=.35,rely=.4)
        
        opt4_label=Label(frm,text="Option 4 :-",font=('Arial',20,'bold'),bg='#2B547E')
        opt4_label.place(relx=.2,rely=.5)
        
        opt4_entry=Entry(frm,font=('Arial',20,'bold'))
        opt4_entry.place(relx=.35,rely=.5)
        
        ans_label=Label(frm,text="Answer :-",font=('Arial',20,'bold'),bg='#2B547E')
        ans_label.place(relx=.2,rely=.60)
        
        ans_entry=Entry(frm,font=('Arial',20,'bold'))
        ans_entry.place(relx=.35,rely=.60)
        
        submit_btn=Label(frm,image=submit_imgtk,bg='#2B547E')
        submit_btn.place(relx=.46,rely=.715)
        submit_btn.bind("<Button>",setques)
        
        logout_btn=Label(frm,image=logout_imgtk,bg='#2B547E')
        logout_btn.place(relx=.71,rely=.03)
        logout_btn.bind("<Button>",logout)
        
    def upload_question():
                
        file=filedialog.askopenfile()
        text=file.read()
        lines=text.split("\n")
        
        for i in range(0,len(lines),6):
            QUES=lines[i:i+6]
            con1=sql.connect(database="quiz.sqlite")
            cur1=con1.cursor()
            cur1.execute("select max(ques_id) from questions")
            qid=cur1.fetchone()[0]
            qid+=1
            con1.close()
            con=sql.connect(database="quiz.sqlite")
            cur=con.cursor()
            cur.execute("insert into questions values(?,?,?,?,?,?,?)",(qid,QUES[0],QUES[1],QUES[2],QUES[3],QUES[4],QUES[5]))
            con.commit()
            con.close()
            messagebox.showinfo("Question","Questions inserted")
        
        def logout(event):
            option=messagebox.askyesno('confirmation','Do you want to logout?')
            if(option==True):
                frm.destroy()
                login_screen()
        
        logout_btn=Label(frm,image=logout_imgtk,bg='grey')
        logout_btn.place(relx=.71,rely=.03)
        logout_btn.bind("<Button>",logout)
        
    def viewuser():
        frm=Frame(win)
        frm.configure(bg='purple')
        frm.place(relx=.21,rely=.15,relwidth=1,relheight=.92)
        
        def logout(event):
            option=messagebox.askyesno('confirmation','Do you want to logout?')
            if(option==True):
                frm.destroy()
                login_screen()
                
        def delete_user(event):
            rowid=tv.focus()
            row=tv.item(rowid,'values')
            if(len(row)==0):
                messagebox.showerror("Delete","please select a row")
            else:
                con=sql.connect(database="quiz.sqlite")
                cur=con.cursor()
                cur.execute("delete from users where username=?",(row[0],))
                con.commit()
                con.close()
                messagebox.showinfo("Delete","Selected User deleted")
                frm.destroy()
                viewuser()
        
        tv=Treeview(frm)
        tv.place(relx=.2,rely=.2,relwidth=.4,height=200)
    
        st=Style()
        st.configure("Treeview.Heading",font=('Arial',16,'bold'),foreground='brown')
    
        sb=Scrollbar(frm,orient="vertical",command=tv.yview)
        sb.place(relx=.596,rely=.2,height=200)
        tv.configure(yscrollcommand=sb.set)
    
        tv['columns']=['1','2']
        tv['show']='headings'
  
        tv.column('1',anchor='c',width=120)
        tv.column('2',anchor='w',width=120)
    
    
        tv.heading('1',text="Username")
        tv.heading('2',text="Password")
    
        con=sql.connect(database='quiz.sqlite')
        cur=con.cursor()
        cur.execute("select * from users")
        ucount=0
        for row in cur:
            ucount+=1
            tv.insert("","end",values=(row[0],row[1]))

        ucount_lbl=Label(frm,text=f"Total Users:{ucount}",font=('Arial',30,'bold'),fg='blue',bg='purple')
        ucount_lbl.place(relx=.3,rely=.1)
        con.close()

        delete_btn=Label(frm,image=delete_imgtk,bg='purple')
        delete_btn.place(relx=.34,rely=.5)
        delete_btn.bind("<Button>",delete_user)
        
        logout_btn=Label(frm,image=logout_imgtk,bg='purple')
        logout_btn.place(relx=.71,rely=.03)
        logout_btn.bind("<Button>",logout)
        
    def viewquest():
        frm=Frame(win)
        frm.configure(bg='orange')
        frm.place(relx=.21,rely=.15,relwidth=1,relheight=.92)
        
        def logout(event):
            option=messagebox.askyesno('confirmation','Do you want to logout?')
            if(option==True):
                frm.destroy()
                login_screen()
                
        def delete_ques(event):
            rowid=tv.focus()
            row=tv.item(rowid,'values')
            if(len(row)==0):
                messagebox.showerror("Delete","please select a row")
            else:
                con=sql.connect(database="quiz.sqlite")
                cur=con.cursor()
                cur.execute("delete from questions where ques_id=?",(row[0]))
                con.commit()
                con.close()
                messagebox.showinfo("Delete","Question deleted")
                frm.destroy()
                viewquest()
        
        tv=Treeview(frm)
        tv.place(relx=.055,rely=.2,relwidth=.682,height=200)
    
        st=Style()
        st.configure("Treeview.Heading",font=('Arial',16,'bold'),foreground='brown')
    
        sb=Scrollbar(frm,orient="vertical",command=tv.yview)
        sb.place(relx=.736,rely=.2,height=200)
        tv.configure(yscrollcommand=sb.set)
        
        sb=Scrollbar(frm,orient="horizontal",command=tv.xview)
        sb.place(relx=.055,rely=.457,relwidth=.6922)
        tv.configure(xscrollcommand=sb.set)
    
        tv['columns']=['1','2','3','4','5','6','7']
        tv['show']='headings'
  
        tv.column('1',anchor='c',width=100)
        tv.column('2',anchor='w',width=350)
        tv.column('3',anchor='c',width=150)
        tv.column('4',anchor='c',width=150)
        tv.column('5',anchor='c',width=150)
        tv.column('6',anchor='c',width=150)
        tv.column('7',anchor='c',width=150)
    
    
        tv.heading('1',text="Quesid")
        tv.heading('2',text="Question")
        tv.heading('3',text="Option-1")
        tv.heading('4',text="Option-2")
        tv.heading('5',text="Option-3")
        tv.heading('6',text="Option-4")
        tv.heading('7',text="Answer")
    
        con=sql.connect(database='quiz.sqlite')
        cur=con.cursor()
        cur.execute("select * from questions")
        qcount=0
        for row in cur:
            qcount+=1
            tv.insert("","end",values=(row[0],row[1],row[2],row[3],row[4],row[5],row[6]))

        qcount_lbl=Label(frm,text=f"Total Questions:{qcount}",font=('Arial',25,'bold'),fg='blue',bg='orange')
        qcount_lbl.place(relx=.3,rely=.1)
        con.close()

        delete_btn=Label(frm,image=delete_imgtk,bg='orange')
        delete_btn.place(relx=.4,rely=.5)
        delete_btn.bind("<Button>",delete_ques)
        
        logout_btn=Label(frm,image=logout_imgtk,bg='orange')
        logout_btn.place(relx=.71,rely=.03)
        logout_btn.bind("<Button>",logout)

    def viewresult():
        frm=Frame(win)
        frm.configure(bg='yellow')
        frm.place(relx=.21,rely=.15,relwidth=1,relheight=.92)   

        def logout(event):
            option=messagebox.askyesno('confirmation','Do you want to logout?')
            if(option==True):
                frm.destroy()
                login_screen()
        tv=Treeview(frm)
        tv.place(relx=.17,rely=.25,width=600,height=150)
    
        sb=ttk.Scrollbar(frm,orient="vertical",command=tv.yview)
        sb.place(relx=.558,rely=.25,height=150)
        tv.configure(yscrollcommand=sb.set)
    
        style = ttk.Style()
        style.configure("Treeview.Heading", font=('Arial',10,'bold'),foreground='brown')
    
        tv['columns']=['1','2','3']
        tv['show']='headings'
    
        tv.column('1',anchor='c',width=250)
        tv.column('2',anchor='c',width=150)
        tv.column('3',anchor='c',width=150)
   
    
        tv.heading('1',text="Date")
        tv.heading('2',text="user")
        tv.heading('3',text="Marks")

    
        con=sql.connect(database='quiz.sqlite')
        cur=con.cursor()
        cur.execute("select * from user_test")
        tcount=0
        for row in cur:
            tcount+=1
            tv.insert("","end",values=(row[2],row[0],row[1]))

        total_label=Label(frm,font=('Arial',25,'bold'),text=f"Total Test Taken:{tcount}",bg='yellow',fg='blue')
        total_label.place(relx=.275,rely=.14)
        con.close()
        
        logout_btn=Label(frm,image=logout_imgtk,bg='yellow')
        logout_btn.place(relx=.71,rely=.03)
        logout_btn.bind("<Button>",logout) 

    logout_btn=Label(frm,image=logout_imgtk,bg='green')
    logout_btn.place(relx=.92,rely=.03)
    logout_btn.bind("<Button>",logout)
        
    welcome_lbl=Label(frm,text="Welcome,Admin.....",font=('',20),bg='green')
    welcome_lbl.place(x=1,y=14)

    setq_btn=Button(frm,width=15,text="Set Questions",font=('',17,'bold'),bd=5,command=set_questions)
    setq_btn.place(relx=.028,rely=.15)

    uploadq_btn=Button(frm,width=15,text="Upload questions",font=('',17,'bold'),bd=5,command=upload_question)
    uploadq_btn.place(relx=.028,rely=.30)

    viewuser_btn=Button(frm,width=15,text="View Users",font=('',17,'bold'),bd=5,command=viewuser)
    viewuser_btn.place(relx=.028,rely=.45)
    
    viewquest_btn=Button(frm,text="View Quest",width=15,font=('',17,'bold'),bd=5,command=viewquest)
    viewquest_btn.place(relx=.028,rely=.6)

    viewresult_btn=Button(frm,text="View Result",width=15,font=('',17,'bold'),bd=5,command=viewresult)
    viewresult_btn.place(relx=.028,rely=.6)
    
def user_screen():
    frm=Frame(win)
    frm.configure(bg='green')
    frm.place(relx=0,rely=.15,relwidth=1,relheight=.92)
    
    def logout(event):
            option=messagebox.askyesno('confirmation','Do you want to logout?')
            if(option==True):
                frm.destroy()
                login_screen()
    
    def start_test():
        frm=Frame(win)
        frm.configure(bg='#2B547E')
        frm.place(relx=.225,rely=.15,relwidth=1,relheight=.92)
        
        def logout(event):
            option=messagebox.askyesno('confirmation','Do you want to logout?')
            if(option==True):
                frm.destroy()
                login_screen()
        
        timer_lbl=Label(frm,font=('Arial',20,'bold'),bg='#2B547E',fg='red')
        timer_lbl.place(relx=.43,rely=.05)
    
        con=sql.connect(database="quiz.sqlite")
        cur=con.cursor()
        cur.execute("select * from questions")
        ques_list=cur.fetchall()
        
    
        var=StringVar(value="yes")
    
        l=Label(frm,bg='#2B547E',font=('Arial',20,'bold'))
        l.place(relx=.1,rely=.2)
    
        rb1=Radiobutton(frm,bg='#2B547E',font=('Arial',15,'bold'))
        rb1.place(relx=.1,rely=.3)
        
        rb2=Radiobutton(frm,bg='#2B547E',font=('Arial',15,'bold'))
        rb2.place(relx=.1,rely=.4)
        
        rb3=Radiobutton(frm,bg='#2B547E',font=('Arial',15,'bold'))
        rb3.place(relx=.1,rely=.5)
        
        rb4=Radiobutton(frm,bg='#2B547E',font=('Arial',15,'bold'))
        rb4.place(relx=.1,rely=.6)
        
        ques_sample=random.sample(ques_list,len(ques_list))
        q1count=0
        marks=0
        flag=0
        def get_quest():
            nonlocal q1count,flag
            flag+=1
            question=ques_sample[q1count]
            q1count+=1
            ans=var.get()
        
            if(flag==1):
                from threading import Thread
                import time
                def timer():
                    for i in range(300,-1,-1):
                        timer_lbl.configure(text=f"Remaining Time: {i//60}:{i%60}")          
                        time.sleep(1)
                        if(i==0):
                            messagebox.showwarning("Timeout","time completed")
                            submit()
                t=Thread(target=timer)
                try:
                    t.start()
                except:
                    pass
        
            def sel():
                nonlocal marks
                user_ans=var.get()
                if(question[6]==user_ans):
                    marks+=1
            def submit():
                messagebox.showinfo("Test",f"Test completed and your Score:{marks}")
                con=sql.connect(database="quiz.sqlite")
                cur=con.cursor()
                day=datetime.now()
                cur.execute("insert into user_test values(?,?,?)",(user[0],marks,str(day)))
                con.commit()
                con.close()
                frm.destroy()
                viewresult()
        
            l.configure(text=f"Ques:{q1count} {question[1]}")
            rb1.configure(text=question[2],variable=var,value=question[2],command=sel)
            rb2.configure(text=question[3],variable=var,value=question[3],command=sel)
            rb3.configure(text=question[4],variable=var,value=question[4],command=sel)
            rb4.configure(text=question[5],variable=var,value=question[5],command=sel)
        
            if(q1count<len(ques_list)):
                reg_btn=Button(frm,text="Next",font=('Arial',17,'bold'),bd=5,width=10,command=get_quest)
                reg_btn.place(relx=.3,rely=.7)
            else:
                reg_btn=Button(frm,text="Submit",font=('Arial',17,'bold'),bd=5,width=10,command=submit)
                reg_btn.place(relx=.3,rely=.7)
    
        get_quest()       
    
        logout_btn=Label(frm,image=logout_imgtk,bg='#2B547E')
        logout_btn.place(relx=.69,rely=.03)
        logout_btn.bind("<Button>",logout)
        
    def viewresult():
        frm=Frame(win)
        frm.configure(bg='grey')
        frm.place(relx=.225,rely=.15,relwidth=1,relheight=.92)
        
        def logout(event):
            option=messagebox.askyesno('confirmation','Do you want to logout?')
            if(option==True):
                frm.destroy()
                login_screen()
        tv=Treeview(frm)
        tv.place(relx=.25,rely=.25,width=400,height=150)
    
        sb=ttk.Scrollbar(frm,orient="vertical",command=tv.yview)
        sb.place(relx=.5,rely=.25,height=150)
        tv.configure(yscrollcommand=sb.set)
    
        style = ttk.Style()
        style.configure("Treeview.Heading", font=('Arial',10,'bold'),foreground='brown')
    
        tv['columns']=['1','2']
        tv['show']='headings'
    
        tv.column('1',anchor='c',width=250)
        tv.column('2',anchor='c',width=150)
   
    
        tv.heading('1',text="Date")
        tv.heading('2',text="Marks")

    
        con=sql.connect(database='quiz.sqlite')
        cur=con.cursor()
        cur.execute("select * from user_test where username=?",(user[0],))
        tcount=0
        for row in cur:
            tcount+=1
            tv.insert("","end",values=(row[2],row[1]))

        total_label=Label(frm,font=('Arial',25,'bold'),text=f"Total Test Taken:{tcount}",bg='grey',fg='blue')
        total_label.place(relx=.275,rely=.14)
        con.close()
        
        logout_btn=Label(frm,image=logout_imgtk,bg='grey')
        logout_btn.place(relx=.69,rely=.03)
        logout_btn.bind("<Button>",logout)
        
    def changepass():
        frm=Frame(win)
        frm.configure(bg='purple')
        frm.place(relx=.225,rely=.15,relwidth=1,relheight=.92)
        
        def logout(event):
            option=messagebox.askyesno('confirmation','Do you want to logout?')
            if(option==True):
                frm.destroy()
                login_screen()
                
        def update(event):
            p=entry_pass.get()
            cp=entry_cpass.get()
        
            if(p==cp):
                con=sql.connect(database="quiz.sqlite")
                cur=con.cursor()
                cur.execute("update users set password=? where username=?",(p,user[0]))
                con.commit()
                con.close()
                messagebox.showinfo("Update","Password Updated")
                frm.destroy()
                login_screen()
            else:
                messagebox.showerror("Update","Password & confim password do not match")
        
        lbl_pass=Label(frm,text="Password:",font=('Arial',20,'bold'),bg='purple')
        lbl_pass.place(relx=.17,rely=.15)
    
        entry_pass=Entry(frm,font=('Arial',20,'bold'),bd=5)
        entry_pass.place(relx=.37,rely=.15)
        entry_pass.focus()
        
        lbl_pass=Label(frm,text="Confirm Password:",font=('Arial',20,'bold'),bg='purple')
        lbl_pass.place(relx=.17,rely=.3)
    
        entry_cpass=Entry(frm,font=('Arial',20,'bold'),bd=5)
        entry_cpass.place(relx=.37,rely=.3)
        
        update_btn=Label(frm,image=update_imgtk,bg='purple')
        update_btn.place(relx=.485,rely=.4)
        update_btn.bind("<Button>",update)
        
        logout_btn=Label(frm,image=logout_imgtk,bg='purple')
        logout_btn.place(relx=.69,rely=.03)
        logout_btn.bind("<Button>",logout)
    
    logout_btn=Label(frm,image=logout_imgtk,bg='green')
    logout_btn.place(relx=.915,rely=.03)
    logout_btn.bind("<Button>",logout)
        
    welcome_lbl=Label(frm,text=f"Welcome,{user[0]}.....",font=('',20),bg='green')
    welcome_lbl.place(x=1,y=14)

    srt_btn=Button(frm,width=17,text="Start Test",font=('',17,'bold'),bd=5,command=start_test)
    srt_btn.place(relx=.028,rely=.15)

    viewresult_btn=Button(frm,width=17,text="View Previous Result",font=('',17,'bold'),bd=5,command=viewresult)
    viewresult_btn.place(relx=.028,rely=.30)

    changepass_btn=Button(frm,width=17,text="Change Password",font=('',17,'bold'),bd=5,command=changepass)
    changepass_btn.place(relx=.028,rely=.45)
    
login_screen()
win.mainloop()


# In[32]:


#con=sql.connect(database="quiz.sqlite")
#cur=con.cursor()
#cur.execute("create table user_test(username text,marks text,day date)")
#cur.execute("create table users(username text primary key,password text)")
#cur.execute("create table questions(ques_id int auto_increment primary key,ques_title text,option1 text,option2 text,option3 text,option4 text,answer text)")
#con.commit()
#con.close()


# In[ ]:




