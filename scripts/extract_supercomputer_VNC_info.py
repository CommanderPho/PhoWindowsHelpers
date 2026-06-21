from playwright.sync_api import sync_playwright

html_content = '''
<html lang="en"><head><style type="text/css">.turbo-progress-bar {
  position: fixed;
  display: block;
  top: 0;
  left: 0;
  height: 3px;
  background: #0076ff;
  z-index: 2147483647;
  transition:
    width 300ms ease-out,
    opacity 150ms 150ms ease-in;
  transform: translate3d(0, 0, 0);
}
</style>
  <title>My Interactive Sessions - Great Lakes on-campus</title>
  <link rel="icon" type="image/x-icon" href="/public/favicon.ico" referrerpolicy="origin">

  <script src="/pun/sys/dashboard/assets/application-e328dc08dca5cb2eae46b553ea259f82da6c7d219b744d943708682efe7f33dd.js" nonce=""></script>
    <script src="/public/chat/chat.js" type="" nonce=""></script>
  <link rel="preload stylesheet" href="/pun/sys/dashboard/assets/application-801d0d6e66023946d95439cc1d31154946cf8d1471ebc6fb1b525d3eb55a7848.css" nonce="" media="all" as="style" type="text/css">
  <style nonce="">
.navbar-dark {
  background-color: #00274c;
}

.navbar-light {
  background-color: #00274c;
}

.navbar-dark ul.navbar-nav li.nav-item > a:focus, .navbar-dark ul.navbar-nav li.nav-item > a.dropdown-toggle.show {
  background-color: #b0b000;
  border-radius: 0.25em;
}
.navbar-light ul.navbar-nav li.nav-item > a:focus, .navbar-light ul.navbar-nav li.nav-item > a.dropdown-toggle.show {
  background-color: #b0b000;
  border-radius: 0.25em;
}
</style>

    <link rel="stylesheet" media="all" href="/public/chat/chat.css" nonce="">

  


  

  <meta name="csrf-param" content="authenticity_token">
<meta name="csrf-token" content="fXjyM8pyrjAvRZRyUSgYm5IraWCBUQDxJhmUYIIGjpNFxJ1Zbl2zpsPAf-8dAuYTFcEd4Cw1WFxeeoIqYPH60g">

  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="profile" content="">

  <meta name="generator" content="Open OnDemand">

  <!-- configuration options exposed to javascript -->
</head><body><div hidden="" id="ood_config" data-max-file-size="10737420000" data-download-enabled="true" data-transfers-path="/pun/sys/dashboard/transfers.json" data-root-path="/pun/sys/dashboard/" data-uppy-locale="&quot;Uppy&quot;" data-bc-dynamic-js="true" data-xdmod-url="" data-base-analytics-path="/pun/sys/dashboard/analytics" data-bc-poll-delay="10000" data-bc-index-url="/pun/sys/dashboard/batch_connect/sessions" data-status-poll-delay="30000" data-status-index-url="/pun/sys/dashboard/system-status" data-support-path="" data-apps-datatable-page-length="10" data-user-home="/home/halechr"></div>



  <header>
    <span class="row">
      <a href="#main_container" class="skip-link">Skip Navigation</a>
    </span>

    <nav class="navbar navbar-expand-md shadow-sm navbar-color navbar-dark">
      <ul class="navbar-nav w-100 align-items-center" role="menubar">
        

<li role="none">
  <a class="navbar-brand navbar-brand-logo" role="menuitem" href="/pun/sys/dashboard/">
    <span>
      Great Lakes on-campus
    </span>
  </a>
</li>

      
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbar" aria-controls="navbar" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>

        <div class="collapse navbar-collapse" id="navbar">
            
            <li class="nav-item dropdown" role="none">
  <a href="#" class="nav-link dropdown-toggle" data-bs-toggle="dropdown" aria-haspopup="true" aria-expanded="false" role="menuitem" title="Files">
    <span> Files</span><span class="caret"></span>
  </a>

  <ul class="dropdown-menu " title="Files" role="menu">
      
  
      <li role="none">
        <a title="Home Directory" class="dropdown-item" role="menuitem" href="/pun/sys/dashboard/files/fs/home/halechr">
  <i id="" class="fas fa-home fa-fw app-icon me-1" title="FontAwesome icon specified: home" aria-hidden="true"></i> Home Directory
</a>
      </li>

  </ul>
</li>
<li class="nav-item dropdown" role="none">
  <a href="#" class="nav-link dropdown-toggle" data-bs-toggle="dropdown" aria-haspopup="true" aria-expanded="false" role="menuitem" title="Jobs">
    <span> Jobs</span><span class="caret"></span>
  </a>

  <ul class="dropdown-menu " title="Jobs" role="menu">
      
  
      <li role="none">
        <a title="Active Jobs" class="dropdown-item" role="menuitem" href="/pun/sys/dashboard/apps/show/activejobs">
  <i id="" class="fa fa-clock-o fa-fw app-icon me-1" title="FontAwesome icon specified: clock-o" aria-hidden="true"></i> Active Jobs
</a>
      </li>
      <li role="none">
        <a title="Job Composer" class="dropdown-item" target="_blank" role="menuitem" href="/pun/sys/dashboard/apps/show/myjobs">
  <i id="" class="fas fa-magic fa-fw app-icon me-1" title="FontAwesome icon specified: magic" aria-hidden="true"></i> Job Composer
</a>
      </li>
      <li role="none">
        <a title="Project Manager" class="dropdown-item" role="menuitem" href="/pun/sys/dashboard/apps/show/projects">
  <i id="" class="fa fa-wrench fa-fw app-icon me-1" title="FontAwesome icon specified: wrench" aria-hidden="true"></i> Project Manager
</a>
      </li>

  </ul>
</li>
<li class="nav-item dropdown" role="none">
  <a href="#" class="nav-link dropdown-toggle" data-bs-toggle="dropdown" aria-haspopup="true" aria-expanded="false" role="menuitem" title="Clusters">
    <span> Clusters</span><span class="caret"></span>
  </a>

  <ul class="dropdown-menu " title="Clusters" role="menu">
      
  
      <li role="none">
        <a title="Module Browser" class="dropdown-item" role="menuitem" href="/pun/sys/dashboard/apps/show/module-browser">
  <i id="" class="fa fa-box fa-fw app-icon me-1" title="FontAwesome icon specified: box" aria-hidden="true"></i> Module Browser
</a>
      </li>
      <li role="none">
        <a title="Great Lakes on-campus Shell Access" class="dropdown-item" target="_blank" role="menuitem" href="/pun/sys/shell/ssh/greatlakes-oncampus.arc-ts.umich.edu">
  <i id="" class="fas fa-terminal fa-fw app-icon me-1" title="FontAwesome icon specified: terminal" aria-hidden="true"></i> Great Lakes on-campus Shell Access
</a>
      </li>
      <li role="none">
        <a title="System Status" class="dropdown-item" role="menuitem" href="/pun/sys/dashboard/apps/show/system-status">
  <i id="" class="fa fa-tachometer fa-fw app-icon me-1" title="FontAwesome icon specified: tachometer" aria-hidden="true"></i> System Status
</a>
      </li>

  </ul>
</li>
<li class="nav-item dropdown" role="none">
  <a href="#" class="nav-link dropdown-toggle" data-bs-toggle="dropdown" aria-haspopup="true" aria-expanded="false" role="menuitem" title="Interactive Apps">
    <span> Interactive Apps</span><span class="caret"></span>
  </a>

  <ul class="dropdown-menu " title="Interactive Apps" role="menu">
      
  <li class="dropdown-header">Applications</li>
      <li role="none">
        <a title="Jupyter + Spark Advanced" class="dropdown-item" role="menuitem" href="/pun/sys/dashboard/batch_connect/sys/arcts_jupyter_spark_advanced/session_contexts/new">
  <img class="app-icon me-1" title="/pun/sys/dashboard/apps/icon/arcts_jupyter_spark_advanced/sys/sys" aria-hidden="true" src="/pun/sys/dashboard/apps/icon/arcts_jupyter_spark_advanced/sys/sys"> Jupyter + Spark Advanced
</a>
      </li>
      <li role="none">
        <a title="Jupyter + Spark Basic" class="dropdown-item" role="menuitem" href="/pun/sys/dashboard/batch_connect/sys/arcts_jupyter_spark_basic/session_contexts/new">
  <img class="app-icon me-1" title="/pun/sys/dashboard/apps/icon/arcts_jupyter_spark_basic/sys/sys" aria-hidden="true" src="/pun/sys/dashboard/apps/icon/arcts_jupyter_spark_basic/sys/sys"> Jupyter + Spark Basic
</a>
      </li>
      <li role="none">
        <a title="Jupyter Notebook" class="dropdown-item" role="menuitem" href="/pun/sys/dashboard/batch_connect/sys/arcts_jupyter_notebook/session_contexts/new">
  <img class="app-icon me-1" title="/pun/sys/dashboard/apps/icon/arcts_jupyter_notebook/sys/sys" aria-hidden="true" src="/pun/sys/dashboard/apps/icon/arcts_jupyter_notebook/sys/sys"> Jupyter Notebook
</a>
      </li>
      <li role="none">
        <a title="JupyterLab" class="dropdown-item" role="menuitem" href="/pun/sys/dashboard/batch_connect/sys/arcts_jupyter_lab/session_contexts/new">
  <img class="app-icon me-1" title="/pun/sys/dashboard/apps/icon/arcts_jupyter_lab/sys/sys" aria-hidden="true" src="/pun/sys/dashboard/apps/icon/arcts_jupyter_lab/sys/sys"> JupyterLab
</a>
      </li>
      <li role="none">
        <a title="MATLAB" class="dropdown-item" role="menuitem" href="/pun/sys/dashboard/batch_connect/sys/arcts_matlab/session_contexts/new">
  <img class="app-icon me-1" title="/pun/sys/dashboard/apps/icon/arcts_matlab/sys/sys" aria-hidden="true" src="/pun/sys/dashboard/apps/icon/arcts_matlab/sys/sys"> MATLAB
</a>
      </li>
      <li role="none">
        <a title="Open WebUI + Ollama" class="dropdown-item" role="menuitem" href="/pun/sys/dashboard/batch_connect/sys/arcts_webui/session_contexts/new">
  <img class="app-icon me-1" title="/pun/sys/dashboard/apps/icon/arcts_webui/sys/sys" aria-hidden="true" src="/pun/sys/dashboard/apps/icon/arcts_webui/sys/sys"> Open WebUI + Ollama
</a>
      </li>
      <li role="none">
        <a title="POSIT Positron" class="dropdown-item" role="menuitem" href="/pun/sys/dashboard/batch_connect/sys/arcts_positron/session_contexts/new">
  <img class="app-icon me-1" title="/pun/sys/dashboard/apps/icon/arcts_positron/sys/sys" aria-hidden="true" src="/pun/sys/dashboard/apps/icon/arcts_positron/sys/sys"> POSIT Positron
</a>
      </li>
      <li role="none">
        <a title="ParaView" class="dropdown-item" role="menuitem" href="/pun/sys/dashboard/batch_connect/sys/arcts_paraview/session_contexts/new">
  <img class="app-icon me-1" title="/pun/sys/dashboard/apps/icon/arcts_paraview/sys/sys" aria-hidden="true" src="/pun/sys/dashboard/apps/icon/arcts_paraview/sys/sys"> ParaView
</a>
      </li>
      <li role="none">
        <a title="RStudio" class="dropdown-item" role="menuitem" href="/pun/sys/dashboard/batch_connect/sys/arcts_rstudio/session_contexts/new">
  <img class="app-icon me-1" title="/pun/sys/dashboard/apps/icon/arcts_rstudio/sys/sys" aria-hidden="true" src="/pun/sys/dashboard/apps/icon/arcts_rstudio/sys/sys"> RStudio
</a>
      </li>
      <li role="none">
        <a title="Stata-MP" class="dropdown-item" role="menuitem" href="/pun/sys/dashboard/batch_connect/sys/arcts_statamp/session_contexts/new">
  <img class="app-icon me-1" title="/pun/sys/dashboard/apps/icon/arcts_statamp/sys/sys" aria-hidden="true" src="/pun/sys/dashboard/apps/icon/arcts_statamp/sys/sys"> Stata-MP
</a>
      </li>
      <li role="none">
        <a title="Visual Studio Code" class="dropdown-item" role="menuitem" href="/pun/sys/dashboard/batch_connect/sys/bc_vscode_server/session_contexts/new">
  <img class="app-icon me-1" title="/pun/sys/dashboard/apps/icon/bc_vscode_server/sys/sys" aria-hidden="true" src="/pun/sys/dashboard/apps/icon/bc_vscode_server/sys/sys"> Visual Studio Code
</a>
      </li>
  <li class="dropdown-divider" role="separator"></li>
  <li class="dropdown-header">Desktops</li>
      <li role="none">
        <a title="Advanced Desktop" class="dropdown-item" role="menuitem" href="/pun/sys/dashboard/batch_connect/sys/bc_desktop_multinode_02/session_contexts/new">
  <i id="" class="fa fa-desktop fa-fw app-icon me-1" title="FontAwesome icon specified: desktop" aria-hidden="true"></i> Advanced Desktop
</a>
      </li>
      <li role="none">
        <a title="Basic Desktop" class="dropdown-item" role="menuitem" href="/pun/sys/dashboard/batch_connect/sys/bc_desktop_basic/session_contexts/new">
  <i id="" class="fa fa-desktop fa-fw app-icon me-1" title="FontAwesome icon specified: desktop" aria-hidden="true"></i> Basic Desktop
</a>
      </li>
      <li role="none">
        <a title="Multinode/MPI Desktop" class="dropdown-item" role="menuitem" href="/pun/sys/dashboard/batch_connect/sys/bc_desktop_multinode_01/session_contexts/new">
  <i id="" class="fa fa-desktop fa-fw app-icon me-1" title="FontAwesome icon specified: desktop" aria-hidden="true"></i> Multinode/MPI Desktop
</a>
      </li>

  </ul>
</li>

            
<li class="nav-item" role="none">
  <a title="My Interactive Sessions" class="nav-link" role="menuitem" href="/pun/sys/dashboard/batch_connect/sessions" aria-current="page">
    <i class="fas fa-window-restore" aria-hidden="true"></i>
    <span class="d-md-none d-xxl-inline"> My Interactive Sessions</span>
  </a>
</li>
            
<li class="nav-item" role="none">
  <a title="All Apps" class="nav-link" role="menuitem" href="/pun/sys/dashboard/apps/index">
    <i class="fas fa-th" aria-hidden="true"></i>
    <span class="d-md-none d-xxl-inline"> All Apps</span>
  </a>
</li>


          <!-- add some space between nav_bar and help_menu -->
          <div class="ms-auto"></div>

            
            <li class="nav-item dropdown" role="none">
  <a href="#" title="Help" class="nav-link dropdown-toggle" data-bs-toggle="dropdown" aria-haspopup="true" aria-expanded="false" role="menuitem">
    <i class="fas fa-question-circle" aria-hidden="true"></i><span class="d-md-none d-xxl-inline"> Help</span><span class="caret"></span>
  </a>

  <ul class="dropdown-menu dropdown-menu-end" role="menu">
    
    
    
    

        
  
      <li role="none">
        <a title="Restart Web Server" class="dropdown-item" role="menuitem" href="/nginx/stop?redir=/pun/sys/dashboard/">
  <i id="" class="fas fa-sync fa-fw app-icon me-1" title="FontAwesome icon specified: sync" aria-hidden="true"></i> Restart Web Server
</a>
      </li>

  </ul>
</li>

            <li class="nav-item" data-container="body" data-bs-toggle="popover" data-content="Logged in as halechr" data-placement="bottom" role="none">
  <a class="nav-link disabled" role="menuitem" title="Logged in as halechr" href="#">
    <i class="fas fa-user" aria-hidden="true"></i><span class="d-md-none d-xxl-inline"> Logged in as halechr</span>
  </a>
</li>
            <li class="nav-item" role="none">
  <a class="nav-link" href="/logout" title="Log Out" role="menuitem">
    <i class="fas fa-sign-out-alt" aria-hidden="true"></i>
    <span class="d-md-none d-xxl-inline"> Log Out</span>
  </a>
</li>
        </div>
      </ul>
    </nav>
  </header>

  <div id="full_page_spinner" class="global-full-page-spinner d-none">
    <div class="spinner-border" role="status"></div>
  </div>

  <div id="main_container" class="container-md content mt-4" role="main">

    

    

    
    
    

    <div id="js-alert-danger-template" class="d-none" aria-hidden="true">
      <div class="alert alert-danger alert-dismissible" role="alert">
        <button type="button" class="btn-close" data-bs-dismiss="alert">
          <span class="sr-only">Close</span>
        </button>
        ALERT_MSG
      </div>
    </div>



    
<script src="/pun/sys/dashboard/assets/batch_connect_sessions-9a8c05bf01bbd6bb76110d716efa89d9b55f93b1fb9a91ff010ff8b2b8ba1207.js" nonce=""></script>

<nav class="breadcrumb-wrapper rounded" aria-label="Breadcrumb">
  <ol class="breadcrumb rounded">
      <li class="breadcrumb-item align-content-center active">
        <a href="/pun/sys/dashboard/">Home</a>
</li>      <li class="breadcrumb-item align-content-center active">
        <a aria-current="page">My Interactive Sessions</a>
</li>  </ol>
  <ul class="breadcrumb-controls pe-3" role="toolbar" aria-label="Page actions">
    <li class="form-check form-switch" title="Toggle notifications">
      <input class="form-check-input" type="checkbox" role="switch" id="notification_toggle" aria-label="Toggle push notifications">
      <label class="form-check-label" for="notification_toggle">
        <i class="fa fa-bell" aria-hidden="true"></i>
        <span class="visually-hidden">Toggle push notifications</span>
      </label>
    </li>
  </ul>
</nav>


<div class="row">
    <nav class="col-md-3" aria-label="Interactive Apps Menu">
        <div id="saved-settings-menu" class="card system-and-shared-apps-header">
    <div class="card-header">Saved Settings</div>
    <div class="list-group list-group-flush">
        <p class="list-group-item mb-0 header border-0">
          <a href="#" class="" data-bs-toggle="collapse" data-bs-target="#saved-settings-0" aria-expanded="true" aria-controls="saved-settings-0">
            <i id="" class="fa fa-desktop fa-fw app-icon" title="FontAwesome icon specified: desktop" aria-hidden="true"></i>
            Basic Desktop
          </a>
        </p>
        <div id="saved-settings-0" class="show saved-settings-list">
            <a class="list-group-item list-group-item-action border-0" href="/pun/sys/dashboard/batch_connect/sys/bc_desktop_basic/settings/cheap-gpu" title="">
              <i id="" class="fa fa-file fa-fw app-icon" aria-hidden="true"></i>
              cheap-gpu
            </a>
            <a class="list-group-item list-group-item-action border-0" href="/pun/sys/dashboard/batch_connect/sys/bc_desktop_basic/settings/default" title="">
              <i id="" class="fa fa-file fa-fw app-icon" aria-hidden="true"></i>
              default
            </a>
            <a class="list-group-item list-group-item-action border-0" href="/pun/sys/dashboard/batch_connect/sys/bc_desktop_basic/settings/high-cpu" title="">
              <i id="" class="fa fa-file fa-fw app-icon" aria-hidden="true"></i>
              high-cpu
            </a>
            <a class="list-group-item list-group-item-action border-0" href="/pun/sys/dashboard/batch_connect/sys/bc_desktop_basic/settings/matlab" title="">
              <i id="" class="fa fa-file fa-fw app-icon" aria-hidden="true"></i>
              matlab
            </a>
            <a class="list-group-item list-group-item-action border-0" href="/pun/sys/dashboard/batch_connect/sys/bc_desktop_basic/settings/pho-debug-cheap" title="">
              <i id="" class="fa fa-file fa-fw app-icon" aria-hidden="true"></i>
              pho-debug-cheap
            </a>
            <a class="list-group-item list-group-item-action border-0" href="/pun/sys/dashboard/batch_connect/sys/bc_desktop_basic/settings/pho-gpu" title="">
              <i id="" class="fa fa-file fa-fw app-icon" aria-hidden="true"></i>
              pho-gpu
            </a>
        </div>
    </div>
  </div>

      
    <div class="card system-and-shared-apps-header">
  <div class="card-header">Interactive Apps</div>
  <div class="list-group list-group-flush">
    <p class="list-group-item mb-0 header border-0">Applications</p>
      <a class="list-group-item list-group-item-action border-0 " data-bs-toggle="popover" data-bs-content="&lt;div class=&quot;ood-appkit markdown&quot;&gt;&lt;p&gt;This app will launch a &lt;a href=&quot;https://spark.apache.org/&quot;&gt;Spark&lt;/a&gt; cluster with integrated &lt;a href=&quot;https://jupyter.org/&quot;&gt;Jupyter&lt;/a&gt; server and &lt;a href=&quot;https://www.python.org/&quot;&gt;Python&lt;/a&gt;. This Advanced version of the app has configurable compute resources so that users can size the Spark cluster to match their needs.&lt;/p&gt;

&lt;p&gt;Each executor uses 3 cpu cores and 15 GB of memory. Decide how many executors you wish to run, then multiply the value by 3 cpu cores and 15 GB of memory and enter these compute resources in the form below. The maximum configurable wall time is 24 hours.&lt;/p&gt;

&lt;p&gt;Note that closing the browser tab of the Jupyter Server or Jupyter Notebook DOES NOT stop the Spark cluster that runs in the background. Your account will continue to accrue charges until you explicitly stop the job or the wall time expires. To stop the job, click the 'Quit' button in the upper right of the Jupyter Server web page.&lt;/p&gt;
&lt;/div&gt;" data-bs-html="true" data-bs-trigger="hover" data-container="body" href="/pun/sys/dashboard/batch_connect/sys/arcts_jupyter_spark_advanced/session_contexts/new" data-bs-original-title="Jupyter + Spark Advanced">
    <img class="app-icon" title="/pun/sys/dashboard/apps/icon/arcts_jupyter_spark_advanced/sys/sys" aria-hidden="true" src="/pun/sys/dashboard/apps/icon/arcts_jupyter_spark_advanced/sys/sys"> Jupyter + Spark Advanced
</a>  <a class="list-group-item list-group-item-action border-0 " data-bs-toggle="popover" data-bs-content="&lt;div class=&quot;ood-appkit markdown&quot;&gt;&lt;p&gt;This app will launch a &lt;a href=&quot;https://spark.apache.org/&quot;&gt;Spark&lt;/a&gt; cluster with integrated &lt;a href=&quot;https://jupyter.org/&quot;&gt;Jupyter&lt;/a&gt; server and &lt;a href=&quot;https://www.python.org/&quot;&gt;Python&lt;/a&gt;. This Basic version of the app provides a Spark cluster with 16 cpu cores and 90 GB of memory. The maximum configurable wall time is 24 hours.&lt;/p&gt;

&lt;p&gt;Note that closing the browser tab of the Jupyter Server or Jupyter Notebook DOES NOT stop the Spark cluster that runs in the background. Your account will continue to accrue charges until you explicitly stop the job or the wall time expires. To stop the job, click the 'Quit' button in the upper right of the Jupyter Server web page.&lt;/p&gt;
&lt;/div&gt;" data-bs-html="true" data-bs-trigger="hover" data-container="body" href="/pun/sys/dashboard/batch_connect/sys/arcts_jupyter_spark_basic/session_contexts/new" data-bs-original-title="Jupyter + Spark Basic">
    <img class="app-icon" title="/pun/sys/dashboard/apps/icon/arcts_jupyter_spark_basic/sys/sys" aria-hidden="true" src="/pun/sys/dashboard/apps/icon/arcts_jupyter_spark_basic/sys/sys"> Jupyter + Spark Basic
</a>  <a class="list-group-item list-group-item-action border-0 " data-bs-toggle="popover" data-bs-content="&lt;div class=&quot;ood-appkit markdown&quot;&gt;&lt;p&gt;This application will launch a &lt;a href=&quot;https://jupyter.org/&quot;&gt;Jupyter Notebook&lt;/a&gt; server using your selected version of &lt;a href=&quot;https://www.python.org/&quot;&gt;Python&lt;/a&gt;.&lt;/p&gt;
&lt;/div&gt;" data-bs-html="true" data-bs-trigger="hover" data-container="body" href="/pun/sys/dashboard/batch_connect/sys/arcts_jupyter_notebook/session_contexts/new" data-bs-original-title="Jupyter Notebook">
    <img class="app-icon" title="/pun/sys/dashboard/apps/icon/arcts_jupyter_notebook/sys/sys" aria-hidden="true" src="/pun/sys/dashboard/apps/icon/arcts_jupyter_notebook/sys/sys"> Jupyter Notebook
</a>  <a class="list-group-item list-group-item-action border-0 " data-bs-toggle="popover" data-bs-content="&lt;div class=&quot;ood-appkit markdown&quot;&gt;&lt;p&gt;This application will launch &lt;a href=&quot;https://jupyter.org/&quot;&gt;JupyterLab&lt;/a&gt; using your selected version of &lt;a href=&quot;https://www.python.org/&quot;&gt;Python&lt;/a&gt;.&lt;/p&gt;
&lt;/div&gt;" data-bs-html="true" data-bs-trigger="hover" data-container="body" href="/pun/sys/dashboard/batch_connect/sys/arcts_jupyter_lab/session_contexts/new" data-bs-original-title="JupyterLab">
    <img class="app-icon" title="/pun/sys/dashboard/apps/icon/arcts_jupyter_lab/sys/sys" aria-hidden="true" src="/pun/sys/dashboard/apps/icon/arcts_jupyter_lab/sys/sys"> JupyterLab
</a>  <a class="list-group-item list-group-item-action border-0 " data-bs-toggle="popover" data-bs-content="&lt;div class=&quot;ood-appkit markdown&quot;&gt;&lt;p&gt;This application provides access to the MATLAB Desktop.  It is limited to
one compute node.&lt;/p&gt;
&lt;/div&gt;" data-bs-html="true" data-bs-trigger="hover" data-container="body" href="/pun/sys/dashboard/batch_connect/sys/arcts_matlab/session_contexts/new" data-bs-original-title="MATLAB">
    <img class="app-icon" title="/pun/sys/dashboard/apps/icon/arcts_matlab/sys/sys" aria-hidden="true" src="/pun/sys/dashboard/apps/icon/arcts_matlab/sys/sys"> MATLAB
</a>  <a class="list-group-item list-group-item-action border-0 " data-bs-toggle="popover" data-bs-content="&lt;div class=&quot;ood-appkit markdown&quot;&gt;&lt;p&gt;This application provides access to the WebUI Desktop.  It is limited to
one compute node. For general information about the WebUI Desktop, please see the
&lt;a href=&quot;https://documentation.its.umich.edu/arc-hpc/open-ondemand/webui-ollama&quot;&gt;WebUI Desktop documentation&lt;/a&gt;.&lt;/p&gt;
&lt;/div&gt;" data-bs-html="true" data-bs-trigger="hover" data-container="body" href="/pun/sys/dashboard/batch_connect/sys/arcts_webui/session_contexts/new" data-bs-original-title="Open WebUI + Ollama">
    <img class="app-icon" title="/pun/sys/dashboard/apps/icon/arcts_webui/sys/sys" aria-hidden="true" src="/pun/sys/dashboard/apps/icon/arcts_webui/sys/sys"> Open WebUI + Ollama
</a>  <a class="list-group-item list-group-item-action border-0 " data-bs-toggle="popover" data-bs-content="&lt;div class=&quot;ood-appkit markdown&quot;&gt;&lt;p&gt;This application provides access to the POSIT Positron IDE.  It is limited to
one compute node.&lt;/p&gt;
&lt;/div&gt;" data-bs-html="true" data-bs-trigger="hover" data-container="body" href="/pun/sys/dashboard/batch_connect/sys/arcts_positron/session_contexts/new" data-bs-original-title="POSIT Positron">
    <img class="app-icon" title="/pun/sys/dashboard/apps/icon/arcts_positron/sys/sys" aria-hidden="true" src="/pun/sys/dashboard/apps/icon/arcts_positron/sys/sys"> POSIT Positron
</a>  <a class="list-group-item list-group-item-action border-0 " data-bs-toggle="popover" data-bs-content="&lt;div class=&quot;ood-appkit markdown&quot;&gt;&lt;p&gt;This application provides access to the ParaView Desktop.  It is limited to
one compute node.&lt;/p&gt;
&lt;/div&gt;" data-bs-html="true" data-bs-trigger="hover" data-container="body" href="/pun/sys/dashboard/batch_connect/sys/arcts_paraview/session_contexts/new" data-bs-original-title="ParaView">
    <img class="app-icon" title="/pun/sys/dashboard/apps/icon/arcts_paraview/sys/sys" aria-hidden="true" src="/pun/sys/dashboard/apps/icon/arcts_paraview/sys/sys"> ParaView
</a>  <a class="list-group-item list-group-item-action border-0 " data-bs-toggle="popover" data-bs-content="&lt;div class=&quot;ood-appkit markdown&quot;&gt;&lt;p&gt;This application provides &lt;a href=&quot;https://www.rstudio.com/&quot;&gt;RStudio&lt;/a&gt;, an integrated development environment
for &lt;a href=&quot;https://www.r-project.org/&quot;&gt;R&lt;/a&gt;.  RStudio will run on a single node using the R module that
you select from the pull down menu.&lt;/p&gt;
&lt;/div&gt;" data-bs-html="true" data-bs-trigger="hover" data-container="body" href="/pun/sys/dashboard/batch_connect/sys/arcts_rstudio/session_contexts/new" data-bs-original-title="RStudio">
    <img class="app-icon" title="/pun/sys/dashboard/apps/icon/arcts_rstudio/sys/sys" aria-hidden="true" src="/pun/sys/dashboard/apps/icon/arcts_rstudio/sys/sys"> RStudio
</a>  <a class="list-group-item list-group-item-action border-0 " data-bs-toggle="popover" data-bs-content="&lt;div class=&quot;ood-appkit markdown&quot;&gt;&lt;p&gt;This application provides access to the Stata-MP Desktop.  It is limited to
one compute node.&lt;/p&gt;
&lt;/div&gt;" data-bs-html="true" data-bs-trigger="hover" data-container="body" href="/pun/sys/dashboard/batch_connect/sys/arcts_statamp/session_contexts/new" data-bs-original-title="Stata-MP">
    <img class="app-icon" title="/pun/sys/dashboard/apps/icon/arcts_statamp/sys/sys" aria-hidden="true" src="/pun/sys/dashboard/apps/icon/arcts_statamp/sys/sys"> Stata-MP
</a>  <a class="list-group-item list-group-item-action border-0 " data-bs-toggle="popover" data-bs-content="&lt;div class=&quot;ood-appkit markdown&quot;&gt;&lt;p&gt;Provides access to a Visual Studio Code web interface. Kindly be aware that utilizing this editor application will initiate a billable job session associated with the specified account.&lt;/p&gt;
&lt;/div&gt;" data-bs-html="true" data-bs-trigger="hover" data-container="body" href="/pun/sys/dashboard/batch_connect/sys/bc_vscode_server/session_contexts/new" data-bs-original-title="Visual Studio Code">
    <img class="app-icon" title="/pun/sys/dashboard/apps/icon/bc_vscode_server/sys/sys" aria-hidden="true" src="/pun/sys/dashboard/apps/icon/bc_vscode_server/sys/sys"> Visual Studio Code
</a>
    <p class="list-group-item mb-0 header border-0">Desktops</p>
      <a class="list-group-item list-group-item-action border-0 " data-bs-toggle="popover" data-bs-content="&lt;div class=&quot;ood-appkit markdown&quot;&gt;&lt;p&gt;This desktop enables you to specify the Slurm tasks per node and the cores per task, which is required 
if you have a job that will use the OpenMP/MPI hybrid model, or if multiple tasks need to be used.&lt;/p&gt;
&lt;/div&gt;" data-bs-html="true" data-bs-trigger="hover" data-container="body" href="/pun/sys/dashboard/batch_connect/sys/bc_desktop_multinode_02/session_contexts/new" data-bs-original-title="Advanced Desktop">
    <i id="" class="fa fa-desktop fa-fw app-icon" title="FontAwesome icon specified: desktop" aria-hidden="true"></i> Advanced Desktop
</a>  <a class="list-group-item list-group-item-action border-0 " data-bs-toggle="popover" data-bs-content="&lt;div class=&quot;ood-appkit markdown&quot;&gt;&lt;p&gt;This is the basic desktop that runs on a single machine.&lt;/p&gt;

&lt;p&gt;See below for information about the maximum number of processors and the
maximum amount of memory available.&lt;/p&gt;
&lt;/div&gt;" data-bs-html="true" data-bs-trigger="hover" data-container="body" href="/pun/sys/dashboard/batch_connect/sys/bc_desktop_basic/session_contexts/new" data-bs-original-title="Basic Desktop">
    <i id="" class="fa fa-desktop fa-fw app-icon" title="FontAwesome icon specified: desktop" aria-hidden="true"></i> Basic Desktop
</a>  <a class="list-group-item list-group-item-action border-0 " data-bs-toggle="popover" data-bs-content="&lt;div class=&quot;ood-appkit markdown&quot;&gt;&lt;p&gt;This desktop will provide access to one or more physical nodes. The most
common use for this desktop is to run programs that use MPI and multiple
physical nodes.&lt;/p&gt;

&lt;p&gt;Make sure your software can use more than one node, and that it is doing
so. You will be charged for what you ask for, not what you use.&lt;/p&gt;
&lt;/div&gt;" data-bs-html="true" data-bs-trigger="hover" data-container="body" href="/pun/sys/dashboard/batch_connect/sys/bc_desktop_multinode_01/session_contexts/new" data-bs-original-title="Multinode/MPI Desktop">
    <i id="" class="fa fa-desktop fa-fw app-icon" title="FontAwesome icon specified: desktop" aria-hidden="true"></i> Multinode/MPI Desktop
</a>
  </div>
</div>



    </nav>
    <div class="col-md-9" role="region" aria-label="Active Sessions">
      <div id="batch_connect_sessions">
    <div id="bc_sessions_content" class="batch-connect sessions" data-should-poll="true">
        <div id="id_ed4c296f-c312-401b-a6c1-b4022b7b919d" class="card session-panel mb-4" data-id="ed4c296f-c312-401b-a6c1-b4022b7b919d" data-hash="2ed6c49c5fbb06bef03a8ae7438504ca2b40b092" data-status="running" data-title="Advanced Desktop" data-job-id="52061993" data-minutes-remaining="97" data-bc-card="true">
  
<div class="card-heading">
  <div class="h5 card-header overflow-auto alert alert-success">
    <a href="/pun/sys/dashboard/batch_connect/sys/bc_desktop_multinode_02/session_contexts/new" class="alert-heading">
      <span class="card-text">Advanced Desktop</span>
    </a>
    <span class="card-text"> (52061993)</span>
    <div class="float-end">
        <span class="badge bg-success rounded-pill">1 node</span>
        <span class="card-text"> | </span>
        <span class="badge bg-success rounded-pill">1 core</span>
        <span class="card-text"> | </span>
      Running
    </div>
  </div>
</div>

  <div class="card-body">
  <div>
    <div class="float-end"><form class="button_to" method="post" action="/pun/sys/dashboard/batch_connect/sessions/ed4c296f-c312-401b-a6c1-b4022b7b919d"><input type="hidden" name="_method" value="delete" autocomplete="off"><button class="btn btn-danger float-end btn-delete" title="Delete Advanced Desktop Session" aria-label="Delete Advanced Desktop Session" data-confirm="Are you sure?" data-toggle="tooltip" data-placement="bottom" type="submit"><i id="" class="fas fa-times-circle fa-fw" title="FontAwesome icon specified: times-circle" aria-hidden="true"></i> <span aria-hidden="true">Delete</span></button><input type="hidden" name="authenticity_token" value="YySQcNuEQJSQEJwArF2zMalar-4VWSBdZQNDgpEiVg1yQWeEQW57nJDP6jkIFOjPs76tOiPqQVsHHeMRE9C76w" autocomplete="off"></form></div>
        <p>
      <strong>Host:</strong>
        <a href="/pun/sys/shell/ssh/gl3039.arc-ts.umich.edu" target="_blank" class="btn btn-primary btn-sm fas fa-terminal">
          gl3039.arc-ts.umich.edu
        </a>
    </p>

    <p>
  <strong>Created at:</strong>
  2026-06-21 01:44:26 EDT
</p>

    <p>
  <strong>Time Remaining:</strong> 1 hour and 37 minutes
</p>

    <p>
  <strong>Session ID:</strong>
  <a target="_blank" href="/pun/sys/dashboard/files/fs/home/halechr/ondemand/data/sys/dashboard/batch_connect/sys/bc_desktop_multinode_02/output/ed4c296f-c312-401b-a6c1-b4022b7b919d">ed4c296f-c312-401b-a6c1-b4022b7b919d</a> 
</p>

    
    
    
    
    <div><ul class="nav nav-tabs"><li class="nav-item active"><a data-bs-toggle="tab" aria-selected="true" class="nav-link active" href="#c_ed4c296f-c312-401b-a6c1-b4022b7b919d_0">noVNC Connection</a></li>
<li class="nav-item "><a data-bs-toggle="tab" class="nav-link " href="#c_ed4c296f-c312-401b-a6c1-b4022b7b919d_1">Native Instructions</a></li></ul><div class="tab-content"><div id="c_ed4c296f-c312-401b-a6c1-b4022b7b919d_0" class="tab-pane ood-appkit markdown active" role="tabpanel"><form action="/pun/sys/dashboard/noVNC-1.3.0/vnc.html" accept-charset="UTF-8" method="get">
 <input type="hidden" name="autoconnect" id="autoconnect" value="true" autocomplete="off">
 <input type="hidden" name="path" id="path" value="rnode/gl3039.arc-ts.umich.edu/29346/websockify" autocomplete="off">
 <input type="hidden" name="resize" id="resize" value="remote" autocomplete="off">
 <input type="hidden" name="password" id="password" value="rD35cTzZ" autocomplete="off">

 <div class="row">
  <div class="col-sm-6">
   <div class="mb-3"><label class="form-label" for="compression">Compression</label><input class="form-control custom-range" type="range" min="1" max="9" value="6" name="compression" id="compression"><small class="form-text text-muted">1 (low) to 9 (high)</small></div>
  </div>
  <div class="col-sm-6">
   <div class="mb-3"><label class="form-label" for="quality">Image Quality</label><input class="form-control custom-range" type="range" min="0" max="9" value="2" name="quality" id="quality"><small class="form-text text-muted">0 (low) to 9 (high)</small></div>
  </div>
 </div>

  <script nonce="">
//<![CDATA[
    // Functions defined in batch_connect_sessions.js
    for(var name of ['compression', 'quality']) {
      tryUpdateSetting(name);
      installSettingHandlers(name);
    }

//]]>
</script>
 <input type="submit" name="commit" value="Launch Advanced Desktop" class="btn btn-primary" formtarget="_blank" data-disable-with="Launch Advanced Desktop">
 <a class="btn btn-light float-end border border-dark" target="_blank" href="/pun/sys/dashboard/noVNC-1.3.0/vnc.html?autoconnect=true&amp;password=mAOpQ97x&amp;path=rnode/gl3039.arc-ts.umich.edu/29346/websockify&amp;resize=downscale">View Only (Share-able Link)</a>
</form></div>
<div id="c_ed4c296f-c312-401b-a6c1-b4022b7b919d_1" class="tab-pane ood-appkit markdown " role="tabpanel">

  <ol>
  <li>
    Download any VNC viewer,
    <a href="https://www.realvnc.com/en/connect/download/viewer/" rel="noopener" target="_blank">RealVNC</a>
    is a good option.
  </li>
  <li>
    <p>
      Copy/paste in your terminal to establish the SSH tunnel:
    </p>
    <pre><code>ssh -f -N -L 22587:gl3039.arc-ts.umich.edu:5901 halechr@greatlakes.arc-ts.umich.edu</code></pre>
    <p>For terminals in Windows you can use: <a href="https://github.com/PowerShell/PowerShell/releases/latest">Powershell</a>,  <a href="https://www.chiark.greenend.org.uk/~sgtatham/putty/">PuTTy</a> and <a href="https://docs.microsoft.com/en-us/windows/wsl/install-win10">Windows Subsystem Linux</a> distributions</p>
  </li>
  <li>
    Open a VNC client and connect to
    <code>localhost:22587</code> within the client
  </li>
  <li>
    <p>Use the VNC password: <code>rD35cTzZ</code></p>
  </li>
</ol>


</div></div></div>
  </div>
</div>

</div>
<div id="id_154a294e-dc24-4457-abf2-c795bf2dda65" class="card session-panel mb-4" data-id="154a294e-dc24-4457-abf2-c795bf2dda65" data-hash="9a62eb0387d28f9058e4b0dc20bded7bcc76a175" data-status="completed" data-title="Advanced Desktop" data-job-id="52059354" data-minutes-remaining="" data-bc-card="true">
  
<div class="card-heading">
  <div class="h5 card-header overflow-auto alert alert-default">
    <a href="/pun/sys/dashboard/batch_connect/sys/bc_desktop_multinode_02/session_contexts/new" class="alert-heading">
      <span class="card-text">Advanced Desktop</span>
    </a>
    <span class="card-text"> (52059354)</span>
    <div class="float-end">
      Completed
        <span class="card-text"> | </span>
        <form class="d-inline edit-session" method="get" action="/pun/sys/dashboard/batch_connect/sys/bc_desktop_multinode_02/session_contexts/new"><button class="btn px-1 py-0 btn-outline-dark full-page-spinner" title="Edit new Advanced Desktop with this session parameters" aria-label="Edit new Advanced Desktop with this session parameters" data-toggle="tooltip" data-placement="left" type="submit"><i id="" class="fas fa-pen fa-fw" aria-hidden="true"></i></button><input type="hidden" name="session_id" value="154a294e-dc24-4457-abf2-c795bf2dda65" autocomplete="off"></form>
        <span class="card-text"> | </span>
        <form class="d-inline relaunch" method="post" action="/pun/sys/dashboard/batch_connect/sys/bc_desktop_multinode_02/session_contexts"><button class="btn px-1 py-0 btn-outline-dark relaunch full-page-spinner" title="Relaunch Advanced Desktop Session" aria-label="Relaunch Advanced Desktop Session" data-toggle="tooltip" data-placement="left" type="submit"><i id="" class="fas fa-sync fa-fw" aria-hidden="true"></i></button><input type="hidden" name="authenticity_token" value="gNWCVuOB_te2YujAB9dTA7x0VpCYKMLzVPk-V_ud4DlF32YVfAD4THLEAoURdDdjluVRnnx0yMNVlCn-_4aflQ" autocomplete="off"><input type="hidden" name="batch_connect_session_context[auto_accounts]" value="kdiba0" autocomplete="off"><input type="hidden" name="batch_connect_session_context[auto_qos]" value="normal" autocomplete="off"><input type="hidden" name="batch_connect_session_context[auto_queues]" value="debug" autocomplete="off"><input type="hidden" name="batch_connect_session_context[bc_email_on_started]" value="0" autocomplete="off"><input type="hidden" name="batch_connect_session_context[bc_num_hours]" value="4" autocomplete="off"><input type="hidden" name="batch_connect_session_context[bc_num_slots]" value="1" autocomplete="off"><input type="hidden" name="batch_connect_session_context[cluster]" value="greatlakes" autocomplete="off"><input type="hidden" name="batch_connect_session_context[cores]" value="1" autocomplete="off"><input type="hidden" name="batch_connect_session_context[custom_partition]" value="standard" autocomplete="off"><input type="hidden" name="batch_connect_session_context[gpus]" value="0" autocomplete="off"><input type="hidden" name="batch_connect_session_context[license]" value="" autocomplete="off"><input type="hidden" name="batch_connect_session_context[mem]" value="32" autocomplete="off"><input type="hidden" name="batch_connect_session_context[modcmds]" value="" autocomplete="off"><input type="hidden" name="batch_connect_session_context[non_gpus_partitions_hidden]" value="standard, standard-oc, largemem, debug, build" autocomplete="off"><input type="hidden" name="batch_connect_session_context[partition_core_hidden]" value="standard/36 standard-oc/36 gpu/40 build/18 debug/36 spgpu/32 gpu_mig40/64 largemem/36 spgpu2/64 viz/40" autocomplete="off"><input type="hidden" name="batch_connect_session_context[partition_mode]" value="select" autocomplete="off"><input type="hidden" name="batch_connect_session_context[qos_mode]" value="default" autocomplete="off"><input type="hidden" name="batch_connect_session_context[setup_file]" value="" autocomplete="off"><input type="hidden" name="batch_connect_session_context[sub_type]" value="env_basic" autocomplete="off"><input type="hidden" name="batch_connect_session_context[tasks]" value="1" autocomplete="off"></form>
    </div>
  </div>
</div>

  <div class="card-body">
  <div>
    <div class="float-end"><form class="button_to" method="post" action="/pun/sys/dashboard/batch_connect/sessions/154a294e-dc24-4457-abf2-c795bf2dda65"><input type="hidden" name="_method" value="delete" autocomplete="off"><button class="btn btn-danger float-end btn-delete" title="Delete Advanced Desktop Session" aria-label="Delete Advanced Desktop Session" data-confirm="Are you sure?" data-toggle="tooltip" data-placement="bottom" type="submit"><i id="" class="fas fa-times-circle fa-fw" title="FontAwesome icon specified: times-circle" aria-hidden="true"></i> <span aria-hidden="true">Delete</span></button><input type="hidden" name="authenticity_token" value="ekREerux8L0CwS_JshY7GrU3pycZPtqnXOD6EHuXbqlDj66kiTdVFd-ai3NjnByyJsp2ZNfar-3goCGKsgYHPA" autocomplete="off"></form></div>
    
    <p>
  <strong>Created at:</strong>
  2026-06-20 22:21:14 EDT
</p>

    <p>
  <strong></strong> 
</p>

    <p>
  <strong>Session ID:</strong>
  <a target="_blank" href="/pun/sys/dashboard/files/fs/home/halechr/ondemand/data/sys/dashboard/batch_connect/sys/bc_desktop_multinode_02/output/154a294e-dc24-4457-abf2-c795bf2dda65">154a294e-dc24-4457-abf2-c795bf2dda65</a> 
</p>

    
    
    
    
    <hr><div class="ood-appkit markdown"><p>
  For debugging purposes, this card will be retained for 6 more days
</p>
</div>
  </div>
</div>

</div>
<div id="id_a9767260-7f2f-41e7-a1fc-9be604ee36ba" class="card session-panel mb-4" data-id="a9767260-7f2f-41e7-a1fc-9be604ee36ba" data-hash="7285f18268563016612b36356336cd3def592dc9" data-status="completed" data-title="Advanced Desktop" data-job-id="52056171" data-minutes-remaining="" data-bc-card="true">
  
<div class="card-heading">
  <div class="h5 card-header overflow-auto alert alert-default">
    <a href="/pun/sys/dashboard/batch_connect/sys/bc_desktop_multinode_02/session_contexts/new" class="alert-heading">
      <span class="card-text">Advanced Desktop</span>
    </a>
    <span class="card-text"> (52056171)</span>
    <div class="float-end">
      Completed
        <span class="card-text"> | </span>
        <form class="d-inline edit-session" method="get" action="/pun/sys/dashboard/batch_connect/sys/bc_desktop_multinode_02/session_contexts/new"><button class="btn px-1 py-0 btn-outline-dark full-page-spinner" title="Edit new Advanced Desktop with this session parameters" aria-label="Edit new Advanced Desktop with this session parameters" data-toggle="tooltip" data-placement="left" type="submit"><i id="" class="fas fa-pen fa-fw" aria-hidden="true"></i></button><input type="hidden" name="session_id" value="a9767260-7f2f-41e7-a1fc-9be604ee36ba" autocomplete="off"></form>
        <span class="card-text"> | </span>
        <form class="d-inline relaunch" method="post" action="/pun/sys/dashboard/batch_connect/sys/bc_desktop_multinode_02/session_contexts"><button class="btn px-1 py-0 btn-outline-dark relaunch full-page-spinner" title="Relaunch Advanced Desktop Session" aria-label="Relaunch Advanced Desktop Session" data-toggle="tooltip" data-placement="left" type="submit"><i id="" class="fas fa-sync fa-fw" aria-hidden="true"></i></button><input type="hidden" name="authenticity_token" value="N9zexsj5Pq0xQZvxDnA8pScohBsKb3Fh-0-kF7rnrVHy1jqFV3g4NvXncbQY01jFDbmDFe4ze1H6IrO-vvzS_Q" autocomplete="off"><input type="hidden" name="batch_connect_session_context[auto_accounts]" value="kdiba0" autocomplete="off"><input type="hidden" name="batch_connect_session_context[auto_qos]" value="normal" autocomplete="off"><input type="hidden" name="batch_connect_session_context[auto_queues]" value="debug" autocomplete="off"><input type="hidden" name="batch_connect_session_context[bc_email_on_started]" value="0" autocomplete="off"><input type="hidden" name="batch_connect_session_context[bc_num_hours]" value="4" autocomplete="off"><input type="hidden" name="batch_connect_session_context[bc_num_slots]" value="1" autocomplete="off"><input type="hidden" name="batch_connect_session_context[cluster]" value="greatlakes" autocomplete="off"><input type="hidden" name="batch_connect_session_context[cores]" value="1" autocomplete="off"><input type="hidden" name="batch_connect_session_context[custom_partition]" value="standard" autocomplete="off"><input type="hidden" name="batch_connect_session_context[gpus]" value="0" autocomplete="off"><input type="hidden" name="batch_connect_session_context[license]" value="" autocomplete="off"><input type="hidden" name="batch_connect_session_context[mem]" value="32" autocomplete="off"><input type="hidden" name="batch_connect_session_context[modcmds]" value="" autocomplete="off"><input type="hidden" name="batch_connect_session_context[non_gpus_partitions_hidden]" value="standard, standard-oc, largemem, debug, build" autocomplete="off"><input type="hidden" name="batch_connect_session_context[partition_core_hidden]" value="standard/36 standard-oc/36 gpu/40 build/18 debug/36 spgpu/32 gpu_mig40/64 largemem/36 spgpu2/64 viz/40" autocomplete="off"><input type="hidden" name="batch_connect_session_context[partition_mode]" value="select" autocomplete="off"><input type="hidden" name="batch_connect_session_context[qos_mode]" value="default" autocomplete="off"><input type="hidden" name="batch_connect_session_context[setup_file]" value="" autocomplete="off"><input type="hidden" name="batch_connect_session_context[sub_type]" value="env_basic" autocomplete="off"><input type="hidden" name="batch_connect_session_context[tasks]" value="1" autocomplete="off"></form>
    </div>
  </div>
</div>

  <div class="card-body">
  <div>
    <div class="float-end"><form class="button_to" method="post" action="/pun/sys/dashboard/batch_connect/sessions/a9767260-7f2f-41e7-a1fc-9be604ee36ba"><input type="hidden" name="_method" value="delete" autocomplete="off"><button class="btn btn-danger float-end btn-delete" title="Delete Advanced Desktop Session" aria-label="Delete Advanced Desktop Session" data-confirm="Are you sure?" data-toggle="tooltip" data-placement="bottom" type="submit"><i id="" class="fas fa-times-circle fa-fw" title="FontAwesome icon specified: times-circle" aria-hidden="true"></i> <span aria-hidden="true">Delete</span></button><input type="hidden" name="authenticity_token" value="70VroZIHrSpZxvzORif7Ja4_lWdAdAeexxE5lzlhupcltOPy6Sx1suXTqv38UUVmaDlxdDSzCFIkTzi6Oh51PA" autocomplete="off"></form></div>
    
    <p>
  <strong>Created at:</strong>
  2026-06-20 19:35:36 EDT
</p>

    <p>
  <strong></strong> 
</p>

    <p>
  <strong>Session ID:</strong>
  <a target="_blank" href="/pun/sys/dashboard/files/fs/home/halechr/ondemand/data/sys/dashboard/batch_connect/sys/bc_desktop_multinode_02/output/a9767260-7f2f-41e7-a1fc-9be604ee36ba">a9767260-7f2f-41e7-a1fc-9be604ee36ba</a> 
</p>

    
    
    
    
    <hr><div class="ood-appkit markdown"><p>
  For debugging purposes, this card will be retained for 6 more days
</p>
</div>
  </div>
</div>

</div>
<div id="id_d03a5b48-3a4e-41da-a88e-125abee71b09" class="card session-panel mb-4" data-id="d03a5b48-3a4e-41da-a88e-125abee71b09" data-hash="db528d741a45b26d1e9c332dcada344b19b74fef" data-status="completed" data-title="Advanced Desktop" data-job-id="52049899" data-minutes-remaining="" data-bc-card="true">
  
<div class="card-heading">
  <div class="h5 card-header overflow-auto alert alert-default">
    <a href="/pun/sys/dashboard/batch_connect/sys/bc_desktop_multinode_02/session_contexts/new" class="alert-heading">
      <span class="card-text">Advanced Desktop</span>
    </a>
    <span class="card-text"> (52049899)</span>
    <div class="float-end">
      Completed
        <span class="card-text"> | </span>
        <form class="d-inline edit-session" method="get" action="/pun/sys/dashboard/batch_connect/sys/bc_desktop_multinode_02/session_contexts/new"><button class="btn px-1 py-0 btn-outline-dark full-page-spinner" title="Edit new Advanced Desktop with this session parameters" aria-label="Edit new Advanced Desktop with this session parameters" data-toggle="tooltip" data-placement="left" type="submit"><i id="" class="fas fa-pen fa-fw" aria-hidden="true"></i></button><input type="hidden" name="session_id" value="d03a5b48-3a4e-41da-a88e-125abee71b09" autocomplete="off"></form>
        <span class="card-text"> | </span>
        <form class="d-inline relaunch" method="post" action="/pun/sys/dashboard/batch_connect/sys/bc_desktop_multinode_02/session_contexts"><button class="btn px-1 py-0 btn-outline-dark relaunch full-page-spinner" title="Relaunch Advanced Desktop Session" aria-label="Relaunch Advanced Desktop Session" data-toggle="tooltip" data-placement="left" type="submit"><i id="" class="fas fa-sync fa-fw" aria-hidden="true"></i></button><input type="hidden" name="authenticity_token" value="vxYBb-Zv7DKLxNkOQyvD4WYp995LHOpXGUuJb_ea_PR6HOUsee7qqU9iM0tViKeBTLjw0K9A4GcYJp7G84GDWA" autocomplete="off"><input type="hidden" name="batch_connect_session_context[auto_accounts]" value="kdiba0" autocomplete="off"><input type="hidden" name="batch_connect_session_context[auto_qos]" value="normal" autocomplete="off"><input type="hidden" name="batch_connect_session_context[auto_queues]" value="debug" autocomplete="off"><input type="hidden" name="batch_connect_session_context[bc_email_on_started]" value="0" autocomplete="off"><input type="hidden" name="batch_connect_session_context[bc_num_hours]" value="4" autocomplete="off"><input type="hidden" name="batch_connect_session_context[bc_num_slots]" value="1" autocomplete="off"><input type="hidden" name="batch_connect_session_context[cluster]" value="greatlakes" autocomplete="off"><input type="hidden" name="batch_connect_session_context[cores]" value="1" autocomplete="off"><input type="hidden" name="batch_connect_session_context[custom_partition]" value="standard" autocomplete="off"><input type="hidden" name="batch_connect_session_context[gpus]" value="0" autocomplete="off"><input type="hidden" name="batch_connect_session_context[license]" value="" autocomplete="off"><input type="hidden" name="batch_connect_session_context[mem]" value="32" autocomplete="off"><input type="hidden" name="batch_connect_session_context[modcmds]" value="" autocomplete="off"><input type="hidden" name="batch_connect_session_context[non_gpus_partitions_hidden]" value="standard, standard-oc, largemem, debug, build" autocomplete="off"><input type="hidden" name="batch_connect_session_context[partition_core_hidden]" value="standard/36 standard-oc/36 gpu/40 build/18 debug/36 spgpu/32 gpu_mig40/64 largemem/36 spgpu2/64 viz/40" autocomplete="off"><input type="hidden" name="batch_connect_session_context[partition_mode]" value="select" autocomplete="off"><input type="hidden" name="batch_connect_session_context[qos_mode]" value="default" autocomplete="off"><input type="hidden" name="batch_connect_session_context[setup_file]" value="" autocomplete="off"><input type="hidden" name="batch_connect_session_context[sub_type]" value="env_basic" autocomplete="off"><input type="hidden" name="batch_connect_session_context[tasks]" value="1" autocomplete="off"></form>
    </div>
  </div>
</div>

  <div class="card-body">
  <div>
    <div class="float-end"><form class="button_to" method="post" action="/pun/sys/dashboard/batch_connect/sessions/d03a5b48-3a4e-41da-a88e-125abee71b09"><input type="hidden" name="_method" value="delete" autocomplete="off"><button class="btn btn-danger float-end btn-delete" title="Delete Advanced Desktop Session" aria-label="Delete Advanced Desktop Session" data-confirm="Are you sure?" data-toggle="tooltip" data-placement="bottom" type="submit"><i id="" class="fas fa-times-circle fa-fw" title="FontAwesome icon specified: times-circle" aria-hidden="true"></i> <span aria-hidden="true">Delete</span></button><input type="hidden" name="authenticity_token" value="nut6jedcvc8BFBqxzbspSoYdjic-q9F2nws-pgAiJOpC9njcZs1kVqKx1pt2kgUUHj4QcFme2yN_SHcnZzCrag" autocomplete="off"></form></div>
    
    <p>
  <strong>Created at:</strong>
  2026-06-20 15:16:22 EDT
</p>

    <p>
  <strong></strong> 
</p>

    <p>
  <strong>Session ID:</strong>
  <a target="_blank" href="/pun/sys/dashboard/files/fs/home/halechr/ondemand/data/sys/dashboard/batch_connect/sys/bc_desktop_multinode_02/output/d03a5b48-3a4e-41da-a88e-125abee71b09">d03a5b48-3a4e-41da-a88e-125abee71b09</a> 
</p>

    
    
    
    
    <hr><div class="ood-appkit markdown"><p>
  For debugging purposes, this card will be retained for 6 more days
</p>
</div>
  </div>
</div>

</div>
<div id="id_113f539e-ecca-4ac4-8119-74a83ee14cd3" class="card session-panel mb-4" data-id="113f539e-ecca-4ac4-8119-74a83ee14cd3" data-hash="d68b555bdf64f4db0040310d001e359bd8c9d707" data-status="completed" data-title="Advanced Desktop" data-job-id="52045846" data-minutes-remaining="" data-bc-card="true">
  
<div class="card-heading">
  <div class="h5 card-header overflow-auto alert alert-default">
    <a href="/pun/sys/dashboard/batch_connect/sys/bc_desktop_multinode_02/session_contexts/new" class="alert-heading">
      <span class="card-text">Advanced Desktop</span>
    </a>
    <span class="card-text"> (52045846)</span>
    <div class="float-end">
      Completed
        <span class="card-text"> | </span>
        <form class="d-inline edit-session" method="get" action="/pun/sys/dashboard/batch_connect/sys/bc_desktop_multinode_02/session_contexts/new"><button class="btn px-1 py-0 btn-outline-dark full-page-spinner" title="Edit new Advanced Desktop with this session parameters" aria-label="Edit new Advanced Desktop with this session parameters" data-toggle="tooltip" data-placement="left" type="submit"><i id="" class="fas fa-pen fa-fw" aria-hidden="true"></i></button><input type="hidden" name="session_id" value="113f539e-ecca-4ac4-8119-74a83ee14cd3" autocomplete="off"></form>
        <span class="card-text"> | </span>
        <form class="d-inline relaunch" method="post" action="/pun/sys/dashboard/batch_connect/sys/bc_desktop_multinode_02/session_contexts"><button class="btn px-1 py-0 btn-outline-dark relaunch full-page-spinner" title="Relaunch Advanced Desktop Session" aria-label="Relaunch Advanced Desktop Session" data-toggle="tooltip" data-placement="left" type="submit"><i id="" class="fas fa-sync fa-fw" aria-hidden="true"></i></button><input type="hidden" name="authenticity_token" value="zMyx2dZjdNczmWA1qn02z1XSHLUaHmT_hPJJRE1_gCEJxlWaSeJyTPc_inC83lKvf0Mbu_5Cbs-Fn17tSWT_jQ" autocomplete="off"><input type="hidden" name="batch_connect_session_context[auto_accounts]" value="kdiba0" autocomplete="off"><input type="hidden" name="batch_connect_session_context[auto_qos]" value="normal" autocomplete="off"><input type="hidden" name="batch_connect_session_context[auto_queues]" value="debug" autocomplete="off"><input type="hidden" name="batch_connect_session_context[bc_email_on_started]" value="0" autocomplete="off"><input type="hidden" name="batch_connect_session_context[bc_num_hours]" value="4" autocomplete="off"><input type="hidden" name="batch_connect_session_context[bc_num_slots]" value="1" autocomplete="off"><input type="hidden" name="batch_connect_session_context[cluster]" value="greatlakes" autocomplete="off"><input type="hidden" name="batch_connect_session_context[cores]" value="1" autocomplete="off"><input type="hidden" name="batch_connect_session_context[custom_partition]" value="standard" autocomplete="off"><input type="hidden" name="batch_connect_session_context[gpus]" value="0" autocomplete="off"><input type="hidden" name="batch_connect_session_context[license]" value="" autocomplete="off"><input type="hidden" name="batch_connect_session_context[mem]" value="32" autocomplete="off"><input type="hidden" name="batch_connect_session_context[modcmds]" value="" autocomplete="off"><input type="hidden" name="batch_connect_session_context[non_gpus_partitions_hidden]" value="standard, standard-oc, largemem, debug, build" autocomplete="off"><input type="hidden" name="batch_connect_session_context[partition_core_hidden]" value="standard/36 standard-oc/36 gpu/40 build/18 debug/36 spgpu/32 gpu_mig40/64 largemem/36 spgpu2/64 viz/40" autocomplete="off"><input type="hidden" name="batch_connect_session_context[partition_mode]" value="select" autocomplete="off"><input type="hidden" name="batch_connect_session_context[qos_mode]" value="default" autocomplete="off"><input type="hidden" name="batch_connect_session_context[setup_file]" value="" autocomplete="off"><input type="hidden" name="batch_connect_session_context[sub_type]" value="env_basic" autocomplete="off"><input type="hidden" name="batch_connect_session_context[tasks]" value="1" autocomplete="off"></form>
    </div>
  </div>
</div>

  <div class="card-body">
  <div>
    <div class="float-end"><form class="button_to" method="post" action="/pun/sys/dashboard/batch_connect/sessions/113f539e-ecca-4ac4-8119-74a83ee14cd3"><input type="hidden" name="_method" value="delete" autocomplete="off"><button class="btn btn-danger float-end btn-delete" title="Delete Advanced Desktop Session" aria-label="Delete Advanced Desktop Session" data-confirm="Are you sure?" data-toggle="tooltip" data-placement="bottom" type="submit"><i id="" class="fas fa-times-circle fa-fw" title="FontAwesome icon specified: times-circle" aria-hidden="true"></i> <span aria-hidden="true">Delete</span></button><input type="hidden" name="authenticity_token" value="EQmLB21hwjtpXXnSQmu--V76z0k_z3hxRMrWENiSrGBb_Du4qqpgWbnsG2bKc5dx33bzDf-f1pJbJOpIeAzQfg" autocomplete="off"></form></div>
    
    <p>
  <strong>Created at:</strong>
  2026-06-20 12:18:37 EDT
</p>

    <p>
  <strong></strong> 
</p>

    <p>
  <strong>Session ID:</strong>
  <a target="_blank" href="/pun/sys/dashboard/files/fs/home/halechr/ondemand/data/sys/dashboard/batch_connect/sys/bc_desktop_multinode_02/output/113f539e-ecca-4ac4-8119-74a83ee14cd3">113f539e-ecca-4ac4-8119-74a83ee14cd3</a> 
</p>

    
    
    
    
    <hr><div class="ood-appkit markdown"><p>
  For debugging purposes, this card will be retained for 6 more days
</p>
</div>
  </div>
</div>

</div>
<div id="id_3877b775-c001-4271-8bc8-cd5826752111" class="card session-panel mb-4" data-id="3877b775-c001-4271-8bc8-cd5826752111" data-hash="8b7b9a4b912f95128e6761e1d944a177e5c3e914" data-status="completed" data-title="Advanced Desktop" data-job-id="52041871" data-minutes-remaining="" data-bc-card="true">
  
<div class="card-heading">
  <div class="h5 card-header overflow-auto alert alert-default">
    <a href="/pun/sys/dashboard/batch_connect/sys/bc_desktop_multinode_02/session_contexts/new" class="alert-heading">
      <span class="card-text">Advanced Desktop</span>
    </a>
    <span class="card-text"> (52041871)</span>
    <div class="float-end">
      Completed
        <span class="card-text"> | </span>
        <form class="d-inline edit-session" method="get" action="/pun/sys/dashboard/batch_connect/sys/bc_desktop_multinode_02/session_contexts/new"><button class="btn px-1 py-0 btn-outline-dark full-page-spinner" title="Edit new Advanced Desktop with this session parameters" aria-label="Edit new Advanced Desktop with this session parameters" data-toggle="tooltip" data-placement="left" type="submit"><i id="" class="fas fa-pen fa-fw" aria-hidden="true"></i></button><input type="hidden" name="session_id" value="3877b775-c001-4271-8bc8-cd5826752111" autocomplete="off"></form>
        <span class="card-text"> | </span>
        <form class="d-inline relaunch" method="post" action="/pun/sys/dashboard/batch_connect/sys/bc_desktop_multinode_02/session_contexts"><button class="btn px-1 py-0 btn-outline-dark relaunch full-page-spinner" title="Relaunch Advanced Desktop Session" aria-label="Relaunch Advanced Desktop Session" data-toggle="tooltip" data-placement="left" type="submit"><i id="" class="fas fa-sync fa-fw" aria-hidden="true"></i></button><input type="hidden" name="authenticity_token" value="4Q22Lb9tD4BdtV71G21iDRDX1IlaZ8UZZsvnwwwR_h4kB1JuIOwJG5kTtLANzgZtOkbTh747zylnpvBqCAqBsg" autocomplete="off"><input type="hidden" name="batch_connect_session_context[auto_accounts]" value="kdiba0" autocomplete="off"><input type="hidden" name="batch_connect_session_context[auto_qos]" value="normal" autocomplete="off"><input type="hidden" name="batch_connect_session_context[auto_queues]" value="debug" autocomplete="off"><input type="hidden" name="batch_connect_session_context[bc_email_on_started]" value="0" autocomplete="off"><input type="hidden" name="batch_connect_session_context[bc_num_hours]" value="4" autocomplete="off"><input type="hidden" name="batch_connect_session_context[bc_num_slots]" value="1" autocomplete="off"><input type="hidden" name="batch_connect_session_context[cluster]" value="greatlakes" autocomplete="off"><input type="hidden" name="batch_connect_session_context[cores]" value="1" autocomplete="off"><input type="hidden" name="batch_connect_session_context[custom_partition]" value="standard" autocomplete="off"><input type="hidden" name="batch_connect_session_context[gpus]" value="0" autocomplete="off"><input type="hidden" name="batch_connect_session_context[license]" value="" autocomplete="off"><input type="hidden" name="batch_connect_session_context[mem]" value="32" autocomplete="off"><input type="hidden" name="batch_connect_session_context[modcmds]" value="" autocomplete="off"><input type="hidden" name="batch_connect_session_context[non_gpus_partitions_hidden]" value="standard, standard-oc, largemem, debug, build" autocomplete="off"><input type="hidden" name="batch_connect_session_context[partition_core_hidden]" value="standard/36 standard-oc/36 gpu/40 build/18 debug/36 spgpu/32 gpu_mig40/64 largemem/36 spgpu2/64 viz/40" autocomplete="off"><input type="hidden" name="batch_connect_session_context[partition_mode]" value="select" autocomplete="off"><input type="hidden" name="batch_connect_session_context[qos_mode]" value="default" autocomplete="off"><input type="hidden" name="batch_connect_session_context[setup_file]" value="" autocomplete="off"><input type="hidden" name="batch_connect_session_context[sub_type]" value="env_basic" autocomplete="off"><input type="hidden" name="batch_connect_session_context[tasks]" value="1" autocomplete="off"></form>
    </div>
  </div>
</div>

  <div class="card-body">
  <div>
    <div class="float-end"><form class="button_to" method="post" action="/pun/sys/dashboard/batch_connect/sessions/3877b775-c001-4271-8bc8-cd5826752111"><input type="hidden" name="_method" value="delete" autocomplete="off"><button class="btn btn-danger float-end btn-delete" title="Delete Advanced Desktop Session" aria-label="Delete Advanced Desktop Session" data-confirm="Are you sure?" data-toggle="tooltip" data-placement="bottom" type="submit"><i id="" class="fas fa-times-circle fa-fw" title="FontAwesome icon specified: times-circle" aria-hidden="true"></i> <span aria-hidden="true">Delete</span></button><input type="hidden" name="authenticity_token" value="rA0uahbHaM7QuyM8iZqCFsSQmQBVZER8SYvONke2SgJD6Iik110vhYegmK9G5t6yDEhiLqgVebDHRRHKZCxSeA" autocomplete="off"></form></div>
    
    <p>
  <strong>Created at:</strong>
  2026-06-20 07:20:55 EDT
</p>

    <p>
  <strong></strong> 
</p>

    <p>
  <strong>Session ID:</strong>
  <a target="_blank" href="/pun/sys/dashboard/files/fs/home/halechr/ondemand/data/sys/dashboard/batch_connect/sys/bc_desktop_multinode_02/output/3877b775-c001-4271-8bc8-cd5826752111">3877b775-c001-4271-8bc8-cd5826752111</a> 
</p>

    
    
    
    
    <hr><div class="ood-appkit markdown"><p>
  For debugging purposes, this card will be retained for 6 more days
</p>
</div>
  </div>
</div>

</div>
<div id="id_18295047-a87c-40b4-9241-62873db0fe1c" class="card session-panel mb-4" data-id="18295047-a87c-40b4-9241-62873db0fe1c" data-hash="4b0a3596e2c9153ac7923e96eb9b1c29e3647b59" data-status="completed" data-title="Advanced Desktop" data-job-id="52039926" data-minutes-remaining="" data-bc-card="true">
  
<div class="card-heading">
  <div class="h5 card-header overflow-auto alert alert-default">
    <a href="/pun/sys/dashboard/batch_connect/sys/bc_desktop_multinode_02/session_contexts/new" class="alert-heading">
      <span class="card-text">Advanced Desktop</span>
    </a>
    <span class="card-text"> (52039926)</span>
    <div class="float-end">
      Completed
        <span class="card-text"> | </span>
        <form class="d-inline edit-session" method="get" action="/pun/sys/dashboard/batch_connect/sys/bc_desktop_multinode_02/session_contexts/new"><button class="btn px-1 py-0 btn-outline-dark full-page-spinner" title="Edit new Advanced Desktop with this session parameters" aria-label="Edit new Advanced Desktop with this session parameters" data-toggle="tooltip" data-placement="left" type="submit"><i id="" class="fas fa-pen fa-fw" aria-hidden="true"></i></button><input type="hidden" name="session_id" value="18295047-a87c-40b4-9241-62873db0fe1c" autocomplete="off"></form>
        <span class="card-text"> | </span>
        <form class="d-inline relaunch" method="post" action="/pun/sys/dashboard/batch_connect/sys/bc_desktop_multinode_02/session_contexts"><button class="btn px-1 py-0 btn-outline-dark relaunch full-page-spinner" title="Relaunch Advanced Desktop Session" aria-label="Relaunch Advanced Desktop Session" data-toggle="tooltip" data-placement="left" type="submit"><i id="" class="fas fa-sync fa-fw" aria-hidden="true"></i></button><input type="hidden" name="authenticity_token" value="pkM4PGipBMIWlqGpB3BSNton-Qy3ShYTBY1vuqAHnZNjSdx_9ygCWdIwS-wR0zZW8Lb-AlMWHCME4HgTpBziPw" autocomplete="off"><input type="hidden" name="batch_connect_session_context[auto_accounts]" value="kdiba0" autocomplete="off"><input type="hidden" name="batch_connect_session_context[auto_qos]" value="normal" autocomplete="off"><input type="hidden" name="batch_connect_session_context[auto_queues]" value="debug" autocomplete="off"><input type="hidden" name="batch_connect_session_context[bc_email_on_started]" value="0" autocomplete="off"><input type="hidden" name="batch_connect_session_context[bc_num_hours]" value="4" autocomplete="off"><input type="hidden" name="batch_connect_session_context[bc_num_slots]" value="1" autocomplete="off"><input type="hidden" name="batch_connect_session_context[cluster]" value="greatlakes" autocomplete="off"><input type="hidden" name="batch_connect_session_context[cores]" value="1" autocomplete="off"><input type="hidden" name="batch_connect_session_context[custom_partition]" value="standard" autocomplete="off"><input type="hidden" name="batch_connect_session_context[gpus]" value="0" autocomplete="off"><input type="hidden" name="batch_connect_session_context[license]" value="" autocomplete="off"><input type="hidden" name="batch_connect_session_context[mem]" value="32" autocomplete="off"><input type="hidden" name="batch_connect_session_context[modcmds]" value="" autocomplete="off"><input type="hidden" name="batch_connect_session_context[non_gpus_partitions_hidden]" value="standard, standard-oc, largemem, debug, build" autocomplete="off"><input type="hidden" name="batch_connect_session_context[partition_core_hidden]" value="standard/36 standard-oc/36 gpu/40 build/18 debug/36 spgpu/32 gpu_mig40/64 largemem/36 spgpu2/64 viz/40" autocomplete="off"><input type="hidden" name="batch_connect_session_context[partition_mode]" value="select" autocomplete="off"><input type="hidden" name="batch_connect_session_context[qos_mode]" value="default" autocomplete="off"><input type="hidden" name="batch_connect_session_context[setup_file]" value="" autocomplete="off"><input type="hidden" name="batch_connect_session_context[sub_type]" value="env_basic" autocomplete="off"><input type="hidden" name="batch_connect_session_context[tasks]" value="1" autocomplete="off"></form>
    </div>
  </div>
</div>

  <div class="card-body">
  <div>
    <div class="float-end"><form class="button_to" method="post" action="/pun/sys/dashboard/batch_connect/sessions/18295047-a87c-40b4-9241-62873db0fe1c"><input type="hidden" name="_method" value="delete" autocomplete="off"><button class="btn btn-danger float-end btn-delete" title="Delete Advanced Desktop Session" aria-label="Delete Advanced Desktop Session" data-confirm="Are you sure?" data-toggle="tooltip" data-placement="bottom" type="submit"><i id="" class="fas fa-times-circle fa-fw" title="FontAwesome icon specified: times-circle" aria-hidden="true"></i> <span aria-hidden="true">Delete</span></button><input type="hidden" name="authenticity_token" value="IFKLdNO-9ATsHdHRXT-B_PYaJRqBZdWfm9a4T4z8wit8WRbiJvBn-co0HzO_T4Sz31cu13YWKXrIcrn8sJKseQ" autocomplete="off"></form></div>
    
    <p>
  <strong>Created at:</strong>
  2026-06-20 02:22:44 EDT
</p>

    <p>
  <strong></strong> 
</p>

    <p>
  <strong>Session ID:</strong>
  <a target="_blank" href="/pun/sys/dashboard/files/fs/home/halechr/ondemand/data/sys/dashboard/batch_connect/sys/bc_desktop_multinode_02/output/18295047-a87c-40b4-9241-62873db0fe1c">18295047-a87c-40b4-9241-62873db0fe1c</a> 
</p>

    
    
    
    
    <hr><div class="ood-appkit markdown"><p>
  For debugging purposes, this card will be retained for 6 more days
</p>
</div>
  </div>
</div>

</div>
<div id="id_a70e247e-5b04-41cb-aadc-59e50864e9e2" class="card session-panel mb-4" data-id="a70e247e-5b04-41cb-aadc-59e50864e9e2" data-hash="4145ab70e0b1c0a639603f8ed1e7020736d3f250" data-status="completed" data-title="Advanced Desktop" data-job-id="52036499" data-minutes-remaining="" data-bc-card="true">
  
<div class="card-heading">
  <div class="h5 card-header overflow-auto alert alert-default">
    <a href="/pun/sys/dashboard/batch_connect/sys/bc_desktop_multinode_02/session_contexts/new" class="alert-heading">
      <span class="card-text">Advanced Desktop</span>
    </a>
    <span class="card-text"> (52036499)</span>
    <div class="float-end">
      Completed
        <span class="card-text"> | </span>
        <form class="d-inline edit-session" method="get" action="/pun/sys/dashboard/batch_connect/sys/bc_desktop_multinode_02/session_contexts/new"><button class="btn px-1 py-0 btn-outline-dark full-page-spinner" title="Edit new Advanced Desktop with this session parameters" aria-label="Edit new Advanced Desktop with this session parameters" data-toggle="tooltip" data-placement="left" type="submit"><i id="" class="fas fa-pen fa-fw" aria-hidden="true"></i></button><input type="hidden" name="session_id" value="a70e247e-5b04-41cb-aadc-59e50864e9e2" autocomplete="off"></form>
        <span class="card-text"> | </span>
        <form class="d-inline relaunch" method="post" action="/pun/sys/dashboard/batch_connect/sys/bc_desktop_multinode_02/session_contexts"><button class="btn px-1 py-0 btn-outline-dark relaunch full-page-spinner" title="Relaunch Advanced Desktop Session" aria-label="Relaunch Advanced Desktop Session" data-toggle="tooltip" data-placement="left" type="submit"><i id="" class="fas fa-sync fa-fw" aria-hidden="true"></i></button><input type="hidden" name="authenticity_token" value="1ncOtlZ_jhSpbXjk58BU0giL823vHL5OVcBuZbqWCMATfer1yf6Ij23LkqHxYzCyIhr0YwtAtH5UrXnMvo13bA" autocomplete="off"><input type="hidden" name="batch_connect_session_context[auto_accounts]" value="kdiba0" autocomplete="off"><input type="hidden" name="batch_connect_session_context[auto_qos]" value="normal" autocomplete="off"><input type="hidden" name="batch_connect_session_context[auto_queues]" value="debug" autocomplete="off"><input type="hidden" name="batch_connect_session_context[bc_email_on_started]" value="0" autocomplete="off"><input type="hidden" name="batch_connect_session_context[bc_num_hours]" value="1" autocomplete="off"><input type="hidden" name="batch_connect_session_context[bc_num_slots]" value="1" autocomplete="off"><input type="hidden" name="batch_connect_session_context[cluster]" value="greatlakes" autocomplete="off"><input type="hidden" name="batch_connect_session_context[cores]" value="1" autocomplete="off"><input type="hidden" name="batch_connect_session_context[custom_partition]" value="standard" autocomplete="off"><input type="hidden" name="batch_connect_session_context[gpus]" value="0" autocomplete="off"><input type="hidden" name="batch_connect_session_context[license]" value="" autocomplete="off"><input type="hidden" name="batch_connect_session_context[mem]" value="32" autocomplete="off"><input type="hidden" name="batch_connect_session_context[modcmds]" value="" autocomplete="off"><input type="hidden" name="batch_connect_session_context[non_gpus_partitions_hidden]" value="standard, standard-oc, largemem, debug, build" autocomplete="off"><input type="hidden" name="batch_connect_session_context[partition_core_hidden]" value="standard/36 standard-oc/36 gpu/40 build/18 debug/36 spgpu/32 gpu_mig40/64 largemem/36 spgpu2/64 viz/40" autocomplete="off"><input type="hidden" name="batch_connect_session_context[partition_mode]" value="select" autocomplete="off"><input type="hidden" name="batch_connect_session_context[qos_mode]" value="default" autocomplete="off"><input type="hidden" name="batch_connect_session_context[setup_file]" value="" autocomplete="off"><input type="hidden" name="batch_connect_session_context[sub_type]" value="env_basic" autocomplete="off"><input type="hidden" name="batch_connect_session_context[tasks]" value="1" autocomplete="off"></form>
    </div>
  </div>
</div>

  <div class="card-body">
  <div>
    <div class="float-end"><form class="button_to" method="post" action="/pun/sys/dashboard/batch_connect/sessions/a70e247e-5b04-41cb-aadc-59e50864e9e2"><input type="hidden" name="_method" value="delete" autocomplete="off"><button class="btn btn-danger float-end btn-delete" title="Delete Advanced Desktop Session" aria-label="Delete Advanced Desktop Session" data-confirm="Are you sure?" data-toggle="tooltip" data-placement="bottom" type="submit"><i id="" class="fas fa-times-circle fa-fw" title="FontAwesome icon specified: times-circle" aria-hidden="true"></i> <span aria-hidden="true">Delete</span></button><input type="hidden" name="authenticity_token" value="d4enPwS5z-GseZxfCOV_9OIW6ne_ByMOGcnf8uKsD2ARWMfM8AfVuh9_VIAZ566AQeq54_Oqg-eWMeWq2IOjTA" autocomplete="off"></form></div>
    
    <p>
  <strong>Created at:</strong>
  2026-06-19 21:45:51 EDT
</p>

    <p>
  <strong></strong> 
</p>

    <p>
  <strong>Session ID:</strong>
  <a target="_blank" href="/pun/sys/dashboard/files/fs/home/halechr/ondemand/data/sys/dashboard/batch_connect/sys/bc_desktop_multinode_02/output/a70e247e-5b04-41cb-aadc-59e50864e9e2">a70e247e-5b04-41cb-aadc-59e50864e9e2</a> 
</p>

    
    
    
    
    <hr><div class="ood-appkit markdown"><p>
  For debugging purposes, this card will be retained for 5 more days
</p>
</div>
  </div>
</div>

</div>
<div id="id_a1521a45-d603-4eb5-ad4e-9b3f978cdde4" class="card session-panel mb-4" data-id="a1521a45-d603-4eb5-ad4e-9b3f978cdde4" data-hash="75d5c2de85cea3c0ca95fba00486e30d479b8ff3" data-status="completed" data-title="Advanced Desktop" data-job-id="52036126" data-minutes-remaining="" data-bc-card="true">
  
<div class="card-heading">
  <div class="h5 card-header overflow-auto alert alert-default">
    <a href="/pun/sys/dashboard/batch_connect/sys/bc_desktop_multinode_02/session_contexts/new" class="alert-heading">
      <span class="card-text">Advanced Desktop</span>
    </a>
    <span class="card-text"> (52036126)</span>
    <div class="float-end">
      Completed
        <span class="card-text"> | </span>
        <form class="d-inline edit-session" method="get" action="/pun/sys/dashboard/batch_connect/sys/bc_desktop_multinode_02/session_contexts/new"><button class="btn px-1 py-0 btn-outline-dark full-page-spinner" title="Edit new Advanced Desktop with this session parameters" aria-label="Edit new Advanced Desktop with this session parameters" data-toggle="tooltip" data-placement="left" type="submit"><i id="" class="fas fa-pen fa-fw" aria-hidden="true"></i></button><input type="hidden" name="session_id" value="a1521a45-d603-4eb5-ad4e-9b3f978cdde4" autocomplete="off"></form>
        <span class="card-text"> | </span>
        <form class="d-inline relaunch" method="post" action="/pun/sys/dashboard/batch_connect/sys/bc_desktop_multinode_02/session_contexts"><button class="btn px-1 py-0 btn-outline-dark relaunch full-page-spinner" title="Relaunch Advanced Desktop Session" aria-label="Relaunch Advanced Desktop Session" data-toggle="tooltip" data-placement="left" type="submit"><i id="" class="fas fa-sync fa-fw" aria-hidden="true"></i></button><input type="hidden" name="authenticity_token" value="HBEGyiVKI-ysaxPT9rQwaqDIY_5f0vUPS3lj3T1KY2fZG-KJussld2jN-ZbgF1QKillk8LuO_z9KFHR0OVEcyw" autocomplete="off"><input type="hidden" name="batch_connect_session_context[auto_accounts]" value="kdiba0" autocomplete="off"><input type="hidden" name="batch_connect_session_context[auto_qos]" value="normal" autocomplete="off"><input type="hidden" name="batch_connect_session_context[auto_queues]" value="debug" autocomplete="off"><input type="hidden" name="batch_connect_session_context[bc_email_on_started]" value="0" autocomplete="off"><input type="hidden" name="batch_connect_session_context[bc_num_hours]" value="1" autocomplete="off"><input type="hidden" name="batch_connect_session_context[bc_num_slots]" value="1" autocomplete="off"><input type="hidden" name="batch_connect_session_context[cluster]" value="greatlakes" autocomplete="off"><input type="hidden" name="batch_connect_session_context[cores]" value="1" autocomplete="off"><input type="hidden" name="batch_connect_session_context[custom_partition]" value="standard" autocomplete="off"><input type="hidden" name="batch_connect_session_context[gpus]" value="0" autocomplete="off"><input type="hidden" name="batch_connect_session_context[license]" value="" autocomplete="off"><input type="hidden" name="batch_connect_session_context[mem]" value="32" autocomplete="off"><input type="hidden" name="batch_connect_session_context[modcmds]" value="" autocomplete="off"><input type="hidden" name="batch_connect_session_context[non_gpus_partitions_hidden]" value="standard, standard-oc, largemem, debug, build" autocomplete="off"><input type="hidden" name="batch_connect_session_context[partition_core_hidden]" value="standard/36 standard-oc/36 gpu/40 build/18 debug/36 spgpu/32 gpu_mig40/64 largemem/36 spgpu2/64 viz/40" autocomplete="off"><input type="hidden" name="batch_connect_session_context[partition_mode]" value="select" autocomplete="off"><input type="hidden" name="batch_connect_session_context[qos_mode]" value="default" autocomplete="off"><input type="hidden" name="batch_connect_session_context[setup_file]" value="" autocomplete="off"><input type="hidden" name="batch_connect_session_context[sub_type]" value="env_basic" autocomplete="off"><input type="hidden" name="batch_connect_session_context[tasks]" value="1" autocomplete="off"></form>
    </div>
  </div>
</div>

  <div class="card-body">
  <div>
    <div class="float-end"><form class="button_to" method="post" action="/pun/sys/dashboard/batch_connect/sessions/a1521a45-d603-4eb5-ad4e-9b3f978cdde4"><input type="hidden" name="_method" value="delete" autocomplete="off"><button class="btn btn-danger float-end btn-delete" title="Delete Advanced Desktop Session" aria-label="Delete Advanced Desktop Session" data-confirm="Are you sure?" data-toggle="tooltip" data-placement="bottom" type="submit"><i id="" class="fas fa-times-circle fa-fw" title="FontAwesome icon specified: times-circle" aria-hidden="true"></i> <span aria-hidden="true">Delete</span></button><input type="hidden" name="authenticity_token" value="4ke63594HlZXWhrCthEPcXeHuqcvo7FWNy7_LsWQFOY24VF-VRHcNAtJc-SWpFh5qvN0bOmkn28orr7K0QY5RA" autocomplete="off"></form></div>
    
    <p>
  <strong>Created at:</strong>
  2026-06-19 20:45:37 EDT
</p>

    <p>
  <strong></strong> 
</p>

    <p>
  <strong>Session ID:</strong>
  <a target="_blank" href="/pun/sys/dashboard/files/fs/home/halechr/ondemand/data/sys/dashboard/batch_connect/sys/bc_desktop_multinode_02/output/a1521a45-d603-4eb5-ad4e-9b3f978cdde4">a1521a45-d603-4eb5-ad4e-9b3f978cdde4</a> 
</p>

    
    
    
    
    <hr><div class="ood-appkit markdown"><p>
  For debugging purposes, this card will be retained for 5 more days
</p>
</div>
  </div>
</div>

</div>
<div id="id_45d8981d-e025-4087-b1bc-c23f580ad8ed" class="card session-panel mb-4" data-id="45d8981d-e025-4087-b1bc-c23f580ad8ed" data-hash="9432c11be2e5bf141da7ef6907f7790a0e0fc730" data-status="completed" data-title="Advanced Desktop" data-job-id="52034602" data-minutes-remaining="" data-bc-card="true">
  
<div class="card-heading">
  <div class="h5 card-header overflow-auto alert alert-default">
    <a href="/pun/sys/dashboard/batch_connect/sys/bc_desktop_multinode_02/session_contexts/new" class="alert-heading">
      <span class="card-text">Advanced Desktop</span>
    </a>
    <span class="card-text"> (52034602)</span>
    <div class="float-end">
      Completed
        <span class="card-text"> | </span>
        <form class="d-inline edit-session" method="get" action="/pun/sys/dashboard/batch_connect/sys/bc_desktop_multinode_02/session_contexts/new"><button class="btn px-1 py-0 btn-outline-dark full-page-spinner" title="Edit new Advanced Desktop with this session parameters" aria-label="Edit new Advanced Desktop with this session parameters" data-toggle="tooltip" data-placement="left" type="submit"><i id="" class="fas fa-pen fa-fw" aria-hidden="true"></i></button><input type="hidden" name="session_id" value="45d8981d-e025-4087-b1bc-c23f580ad8ed" autocomplete="off"></form>
        <span class="card-text"> | </span>
        <form class="d-inline relaunch" method="post" action="/pun/sys/dashboard/batch_connect/sys/bc_desktop_multinode_02/session_contexts"><button class="btn px-1 py-0 btn-outline-dark relaunch full-page-spinner" title="Relaunch Advanced Desktop Session" aria-label="Relaunch Advanced Desktop Session" data-toggle="tooltip" data-placement="left" type="submit"><i id="" class="fas fa-sync fa-fw" aria-hidden="true"></i></button><input type="hidden" name="authenticity_token" value="7AV-MmYonZQeD9X3TESsUaa4UQ5L-dLV0UqyOkgOOVopD5px-ambD9qpP7Ja58gxjClWAK-l2OXQJ6WTTBVG9g" autocomplete="off"><input type="hidden" name="batch_connect_session_context[auto_accounts]" value="kdiba0" autocomplete="off"><input type="hidden" name="batch_connect_session_context[auto_qos]" value="normal" autocomplete="off"><input type="hidden" name="batch_connect_session_context[auto_queues]" value="debug" autocomplete="off"><input type="hidden" name="batch_connect_session_context[bc_email_on_started]" value="0" autocomplete="off"><input type="hidden" name="batch_connect_session_context[bc_num_hours]" value="1" autocomplete="off"><input type="hidden" name="batch_connect_session_context[bc_num_slots]" value="1" autocomplete="off"><input type="hidden" name="batch_connect_session_context[cluster]" value="greatlakes" autocomplete="off"><input type="hidden" name="batch_connect_session_context[cores]" value="1" autocomplete="off"><input type="hidden" name="batch_connect_session_context[custom_partition]" value="standard" autocomplete="off"><input type="hidden" name="batch_connect_session_context[gpus]" value="0" autocomplete="off"><input type="hidden" name="batch_connect_session_context[license]" value="" autocomplete="off"><input type="hidden" name="batch_connect_session_context[mem]" value="32" autocomplete="off"><input type="hidden" name="batch_connect_session_context[modcmds]" value="" autocomplete="off"><input type="hidden" name="batch_connect_session_context[non_gpus_partitions_hidden]" value="standard, standard-oc, largemem, debug, build" autocomplete="off"><input type="hidden" name="batch_connect_session_context[partition_core_hidden]" value="standard/36 standard-oc/36 gpu/40 build/18 debug/36 spgpu/32 gpu_mig40/64 largemem/36 spgpu2/64 viz/40" autocomplete="off"><input type="hidden" name="batch_connect_session_context[partition_mode]" value="select" autocomplete="off"><input type="hidden" name="batch_connect_session_context[qos_mode]" value="default" autocomplete="off"><input type="hidden" name="batch_connect_session_context[setup_file]" value="" autocomplete="off"><input type="hidden" name="batch_connect_session_context[sub_type]" value="env_basic" autocomplete="off"><input type="hidden" name="batch_connect_session_context[tasks]" value="1" autocomplete="off"></form>
    </div>
  </div>
</div>

  <div class="card-body">
  <div>
    <div class="float-end"><form class="button_to" method="post" action="/pun/sys/dashboard/batch_connect/sessions/45d8981d-e025-4087-b1bc-c23f580ad8ed"><input type="hidden" name="_method" value="delete" autocomplete="off"><button class="btn btn-danger float-end btn-delete" title="Delete Advanced Desktop Session" aria-label="Delete Advanced Desktop Session" data-confirm="Are you sure?" data-toggle="tooltip" data-placement="bottom" type="submit"><i id="" class="fas fa-times-circle fa-fw" title="FontAwesome icon specified: times-circle" aria-hidden="true"></i> <span aria-hidden="true">Delete</span></button><input type="hidden" name="authenticity_token" value="krJhkC8j3rF1feDqNlWMVo5iCKlXT8daKwV-qlj4_olzhhJVA3gagRiZrHtNB7KoTBeSi_qwTlJotlWzddS9qw" autocomplete="off"></form></div>
    
    <p>
  <strong>Created at:</strong>
  2026-06-19 18:46:42 EDT
</p>

    <p>
  <strong></strong> 
</p>

    <p>
  <strong>Session ID:</strong>
  <a target="_blank" href="/pun/sys/dashboard/files/fs/home/halechr/ondemand/data/sys/dashboard/batch_connect/sys/bc_desktop_multinode_02/output/45d8981d-e025-4087-b1bc-c23f580ad8ed">45d8981d-e025-4087-b1bc-c23f580ad8ed</a> 
</p>

    
    
    
    
    <hr><div class="ood-appkit markdown"><p>
  For debugging purposes, this card will be retained for 5 more days
</p>
</div>
  </div>
</div>

</div>
<div id="id_5ac0bef0-a04a-4517-9e9b-ce071daa4864" class="card session-panel mb-4" data-id="5ac0bef0-a04a-4517-9e9b-ce071daa4864" data-hash="d17da5413968fbd9ecc11d9466b5cbb6ef6c1795" data-status="completed" data-title="Advanced Desktop" data-job-id="52033434" data-minutes-remaining="" data-bc-card="true">
  
<div class="card-heading">
  <div class="h5 card-header overflow-auto alert alert-default">
    <a href="/pun/sys/dashboard/batch_connect/sys/bc_desktop_multinode_02/session_contexts/new" class="alert-heading">
      <span class="card-text">Advanced Desktop</span>
    </a>
    <span class="card-text"> (52033434)</span>
    <div class="float-end">
      Completed
        <span class="card-text"> | </span>
        <form class="d-inline edit-session" method="get" action="/pun/sys/dashboard/batch_connect/sys/bc_desktop_multinode_02/session_contexts/new"><button class="btn px-1 py-0 btn-outline-dark full-page-spinner" title="Edit new Advanced Desktop with this session parameters" aria-label="Edit new Advanced Desktop with this session parameters" data-toggle="tooltip" data-placement="left" type="submit"><i id="" class="fas fa-pen fa-fw" aria-hidden="true"></i></button><input type="hidden" name="session_id" value="5ac0bef0-a04a-4517-9e9b-ce071daa4864" autocomplete="off"></form>
        <span class="card-text"> | </span>
        <form class="d-inline relaunch" method="post" action="/pun/sys/dashboard/batch_connect/sys/bc_desktop_multinode_02/session_contexts"><button class="btn px-1 py-0 btn-outline-dark relaunch full-page-spinner" title="Relaunch Advanced Desktop Session" aria-label="Relaunch Advanced Desktop Session" data-toggle="tooltip" data-placement="left" type="submit"><i id="" class="fas fa-sync fa-fw" aria-hidden="true"></i></button><input type="hidden" name="authenticity_token" value="WWB_4QqanbOPKwkinpuaUZb3CjwQHWwVqIIa--44Oj2capuilRubKEuN42eIOP4xvGYNMvRBZiWp7w1S6iNFkQ" autocomplete="off"><input type="hidden" name="batch_connect_session_context[auto_accounts]" value="kdiba0" autocomplete="off"><input type="hidden" name="batch_connect_session_context[auto_qos]" value="normal" autocomplete="off"><input type="hidden" name="batch_connect_session_context[auto_queues]" value="debug" autocomplete="off"><input type="hidden" name="batch_connect_session_context[bc_email_on_started]" value="0" autocomplete="off"><input type="hidden" name="batch_connect_session_context[bc_num_hours]" value="1" autocomplete="off"><input type="hidden" name="batch_connect_session_context[bc_num_slots]" value="1" autocomplete="off"><input type="hidden" name="batch_connect_session_context[cluster]" value="greatlakes" autocomplete="off"><input type="hidden" name="batch_connect_session_context[cores]" value="1" autocomplete="off"><input type="hidden" name="batch_connect_session_context[custom_partition]" value="standard" autocomplete="off"><input type="hidden" name="batch_connect_session_context[gpus]" value="0" autocomplete="off"><input type="hidden" name="batch_connect_session_context[license]" value="" autocomplete="off"><input type="hidden" name="batch_connect_session_context[mem]" value="1" autocomplete="off"><input type="hidden" name="batch_connect_session_context[modcmds]" value="" autocomplete="off"><input type="hidden" name="batch_connect_session_context[non_gpus_partitions_hidden]" value="standard, standard-oc, largemem, debug, build" autocomplete="off"><input type="hidden" name="batch_connect_session_context[partition_core_hidden]" value="standard/36 standard-oc/36 gpu/40 build/18 debug/36 spgpu/32 gpu_mig40/64 largemem/36 spgpu2/64 viz/40" autocomplete="off"><input type="hidden" name="batch_connect_session_context[partition_mode]" value="select" autocomplete="off"><input type="hidden" name="batch_connect_session_context[qos_mode]" value="default" autocomplete="off"><input type="hidden" name="batch_connect_session_context[setup_file]" value="" autocomplete="off"><input type="hidden" name="batch_connect_session_context[sub_type]" value="env_basic" autocomplete="off"><input type="hidden" name="batch_connect_session_context[tasks]" value="1" autocomplete="off"></form>
    </div>
  </div>
</div>

  <div class="card-body">
  <div>
    <div class="float-end"><form class="button_to" method="post" action="/pun/sys/dashboard/batch_connect/sessions/5ac0bef0-a04a-4517-9e9b-ce071daa4864"><input type="hidden" name="_method" value="delete" autocomplete="off"><button class="btn btn-danger float-end btn-delete" title="Delete Advanced Desktop Session" aria-label="Delete Advanced Desktop Session" data-confirm="Are you sure?" data-toggle="tooltip" data-placement="bottom" type="submit"><i id="" class="fas fa-times-circle fa-fw" title="FontAwesome icon specified: times-circle" aria-hidden="true"></i> <span aria-hidden="true">Delete</span></button><input type="hidden" name="authenticity_token" value="AoUO4W3XimBKuLKk5zlT8T2f-iIZ3fia3foIDuGWzXSidfVN7enf6t_f1CrRFc3iZojUSuRWtummpxPrU4qZLw" autocomplete="off"></form></div>
    
    <p>
  <strong>Created at:</strong>
  2026-06-19 18:17:52 EDT
</p>

    <p>
  <strong></strong> 
</p>

    <p>
  <strong>Session ID:</strong>
  <a target="_blank" href="/pun/sys/dashboard/files/fs/home/halechr/ondemand/data/sys/dashboard/batch_connect/sys/bc_desktop_multinode_02/output/5ac0bef0-a04a-4517-9e9b-ce071daa4864">5ac0bef0-a04a-4517-9e9b-ce071daa4864</a> 
</p>

    
    
    
    
    <hr><div class="ood-appkit markdown"><p>
  For debugging purposes, this card will be retained for 5 more days
</p>
</div>
  </div>
</div>

</div>

    </div>
  </div>
    </div>
</div>
<div id="full-page-spinner" class="d-none">
  <div class="spinner-border" role="status"></div>
</div>


  </div><!-- /.container -->

  <footer class="d-flex m-0 mt-4 justify-content-between align-items-center p-4">
  <div class="me-2">
    <a href="https://openondemand.org">
      <img class="footer-logo" alt="Powered by Open OnDemand" height="40px" src="/pun/sys/dashboard/assets/OpenOnDemand_powered_by_RGB-cb3aad5ff5350c7994f250fb334ddcc72e343233ce99eb71fda93beddd76a847.svg">
</a>  </div>
  <span id="ood_version">OnDemand version: 4.1.5<br><a href="https://openondemand.org/licensing">Software License Notice</a></span>
</footer>

  <div id="aria_live_region" class="visually-hidden" aria-live="polite"></div>


<button id="arc-chat-bubble" title="ARC HPC Intelligent Engine (ARCHIE)"></button><div id="arc-chat-window" style="display: none;"><div class="chat-header"><span>ARC HPC Intelligent Engine (ARCHIE)<span class="chat-beta-badge">beta</span></span><button class="chat-new-conversation" title="Start a new conversation">New Conversation</button><button class="chat-close">×</button></div><div id="chat-messages" class="chat-messages"></div><div class="chat-input-container"><div id="chat-suggestions" class="chat-suggestions"></div><div id="chat-loading" class="chat-loading" style="display: none;">Assistant is thinking...</div><textarea id="chat-input" rows="1" placeholder="Ask a question... (Shift+Enter for new line)"></textarea><button>Send</button></div><div class="chat-resize-handle" title="Drag to resize"></div></div></body></html>

'''

""" Extracted contents of the 'Native Instructions" tab:
ssh -f -N -L 22587:gl3039.arc-ts.umich.edu:5901 halechr@greatlakes.arc-ts.umich.edu
localhost:22587
rD35cTzZ
"""

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.set_content(html_content)

    # 1. Force the Native Instructions tab to become active
    # 2. Disable the specific script that causes the toggle
    page.evaluate("document.querySelector('a[href*=\"_1\"]').click()")
    page.evaluate("window.onhashchange = null; clearInterval(window.pollInterval);")

    # Now extract the content
    password = page.inner_text("xpath=//div[contains(@id, '_1')]//code[contains(text(), 'rD')]")
    print(f"Extracted Password: {password}")

