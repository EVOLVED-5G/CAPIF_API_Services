provider "kubernetes" {
  config_path    = "kubeconfig"
  config_context = "evolved5g/openshift-epg-hi-inet:443/system:serviceaccount:evolved5g:jenkins"
  insecure       = true
}
