provider "kubernetes" {
config_path = "~/kubeconfig"
config_context = "evol5-capif/api-ocp-epg-hi-inet:6443/system:serviceaccount:evol5-capif:deployer"
insecure = true
}