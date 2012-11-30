# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a samples controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################
@auth.requires_membership('Administrator')
def index():
    emp=db().select(db.Employee.ALL, orderby=db.Employee.Importance_val)
    
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html
    """
    form=crud.create(db.Employee)
    response.flash = "Employee Details"
    return dict(form=form,emp=emp)

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())





@auth.requires_signature()
def data():
    """
    http://..../[app]/default/data/tables
    http://..../[app]/default/data/create/[table]
    http://..../[app]/default/data/read/[table]/[id]
    http://..../[app]/default/data/update/[table]/[id]
    http://..../[app]/default/data/delete/[table]/[id]
    http://..../[app]/default/data/select/[table]
    http://..../[app]/default/data/search/[table]
    but URLs must be signed, i.e. linked with
      A('table',_href=URL('data/tables',user_signature=True))
    or with the signed load operator
      LOAD('default','data.load',args='tables',ajax=True,user_signature=True)
    """
    return dict(form=crud())

def graph():
    empl=db.Employee(request.args(0))
    return dict(empl=empl)  
 


def relate():
   response.flash= "Define Relation"
   form=crud.create(db.Relation)
   return dict(form=form)

def dele():
   db.Employee.truncate()
   db.Relation.truncate()
   redirect(URL("index"))
c=[]
rep=[]
vis=[]
ed=[]
p={}
q={}
def kruskal():
    
    lis = db().select(db.Relation.ALL)
    emp=db().select(db.Employee.ALL, orderby=db.Employee.Name)
    counts=len(emp)
    for i in xrange(counts+1):
       c.append([])
       vis.append([])
       rep.append(i)
       ed.append([])
       for j in xrange(counts+1):
          c[i].append(0)
          vis[i].append(0)
          ed[i].append(0)
    for li in lis:
       a=li.Emp1_id
       b=li.Emp2_id
       c[a][b]=1
       
    cou=0   
    while cou !=counts:
        min=100
        for i in xrange(counts+1):
            for j in xrange(counts+1):
                if c[i][j]!=0 and vis[i][j]==0:
                    if rep[i]!=rep[j]:
                               vis[i][j]=1
                               ed[i][j]=1
                               count1=0
                               count2=0
                               for k in xrange(counts+1):
                                        if rep[k]==rep[i]:
                                            count1=count1+1
                                        if rep[k]==rep[j]:
                                            count2=count2+1
                               if count1<count2:
                                           for k in xrange(counts+1):
                                                if rep[k]==rep[i] and k!=i:
                                                    rep[k]=rep[j]
                                           rep[i]=rep[j]
                               else:
                                        for k in xrange(counts+1):
                                                   if rep[k]==rep[j] and k!=j:
                                                        rep[k]=rep[i]
                                        rep[j]=rep[i]

                    else:
                        vis[i][j]=1
        cou=0
        for k in xrange(counts+1):
            if rep[k]==rep[1]:
                    cou=cou+1
        k=0            
        for i in xrange(counts+1):
                for j in xrange(counts+1):
                      if ed[i][j]==1:
                           p[k]=i
                           q[k]=j
                           k=k+1 
    v=[0]*k
    for i in xrange(k):
       flag=0
       for j in xrange(k):
          if p[i]==q[j]:
             flag=1
             break
       if flag==0:
          break
    
    file=open('applications/project/controllers/myfile.txt','w')      
    fil(p,q,v,p[i],k)   
    for j in xrange(k):
        if v[j]==0:
            fil(p,q,v,p[j],k)
                    
    #file = open('applications/project/controllers/myfile.txt','w')
    #for i in xrange(counts+1):
     #   co=0  
    
    #    file = open('applications/project/controllers/myfile.txt','a')
      #  for j in xrange(k):
       #     file = open('applications/project/controllers/myfile.txt','a')
        #    if p[j]==i:
         #     co=co+1
          #    if co==1:
           #     file.write("{\"name\":\"%d\", " %p[j])
            #    file.write("\"children\":[{\"name\":\"%d\"}" %q[j] )
             # else:
              #  file.write(",{\"name\":\"%d\"}" %q[j])
                #file.write('children=q[j]')
               # file.close()     
       # if co>0:
        # file.write("]")
         #file.write("}")                                               
    return dict(p=p,q=q)
def fil(p,q,v,k,t):
  flag=0
  for i in xrange(t):
       fl=0
       for j in xrange(t):
           if p[j]==k and v[j]==1:
              fl=1
              break
       if p[i]==k and fl==0:
           flag=1
           file=open('applications/project/controllers/myfile.txt','a')
           file.write("{\"name\":\"%d\"," %p[i])
           v[i]=1
           file.write("\"children\":[")
           file.close()
           fil(p,q,v,q[i],t)
       if p[i]==k and fl==1:
           flag=1
           v[i]=1
           file=open('applications/project/controllers/myfile.txt','a')
           file.write("{\"name\":\"%d\"}" %q[i])
           file.close()
           fil(p,q,v,q[i],t)
  #if flag==0:
   # file=open('applications/project/controllers/myfile.txt','a')
    #file.write("{\"name\":\"%d\"}," %k)
    #file.close()
  #elif fl==0:
   # for i in xrange(t):
    #   if p[i]==k:
     #    file=open('applications/project/controllers/myfile.txt','a')
      #   file.write("{\"name\":\"%d\"}," %q[i])
       #  file.close()
