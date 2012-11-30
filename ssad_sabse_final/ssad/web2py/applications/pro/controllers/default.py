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

def check_access():
    return 'true' if auth.is_logged_in() else 'false'
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
 
def index1():
   response.kruskal = [(T('Index'), False, 'http://www.google.com')]

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
    file=open('applications/pro/controllers/inp.txt','w')
    file.write("%d\n" %k)
    ro={}
    for i in xrange(k):
        ro=db(db.Employee.id==p[i]).select(db.Employee.Designation)
        d= ro[0]['Designation']
        file.write("%s " %d)
        ro=db((db.Employee.id==q[i])).select(db.Employee.Designation)
        d= ro[0]['Designation']
        file.write("%s\n" %d)
    file.close()
    import sys
    graph = {}
    f=open('applications/pro/controllers/inp.txt','r')
    lines = int(f.readline())
    indegree = {}
    for i in range(lines):
        edge = (f.readline()).split(" ")
        if len(edge) != 2:
            print "Error in the input format"
            sys.exit()
        if graph.has_key(edge[0]):
            edge[1]=edge[1][0:len(edge[1])-1]
            graph[edge[0]].append(edge[1])
        else:
            edge[1]=edge[1][0:len(edge[1])-1]
            graph[edge[0]] = [edge[1],]
        if indegree.has_key(edge[0]) == False:
            indegree[edge[0]] = 0
        if indegree.has_key(edge[1]):
            indegree[edge[1]] += 1
        else:
            indegree[edge[1]] = 1
    root  = ""
    for v in indegree:
        if indegree[v] == 0:
            root = v
            break

    def dfs(root):
        ret = {}
        ret["name"] = root
        if graph.has_key(root) == False :
            return ret
        vertices = graph[root]
        ret["children"] = []
        for vertex in vertices:
            ret["children"].append(dfs(vertex))
        return ret
        
    file=open('applications/pro/controllers/trig_map.json','w')
    file.write("%s" %dfs(root))
    file.close()
    f=open('applications/pro/controllers/trig_map.json','r')
    l=f.readlines()
    str=l[0]
    f.close()
    f=open('applications/pro/controllers/trig_map.json','w')
    f.write("%s" %str.replace("'","\""))
    f.close()
    
    
    return dict(p=p,q=q)
