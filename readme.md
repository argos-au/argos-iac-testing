# Infrastructure as Code testing by ARGOS

This repository is used to build the free to the community Infrastructure as Code (IaC) test API by <a href="https://argos-security.io">ARGOS</a> accessible at https://test-iac.argos-security.io/api/iac-test

The API is provided without guarantee and free of charge.
ARGOS does not store any information about templates tested.

## Supported Templates

- Azure Resource Manager (ARM) templates in JSON format
- Amazon Web Services (AWS) templates in JSON/YAML format

## Dependencies

- Azure Functions runtime
- python 3.8
- <a href="https://github.com/bridgecrewio/checkov">checkov</a>

## Build

You can run the Function locally using the Azure Functions `func` cli or by building the `Dockerfile`.

`docker build -t <dockerImageName> .`

## Run

Once the `func` cli has built and started the Function or the Docker image is built we can call the API.
Start the docker image like this:

`docker run -p 8080:80 <dockerImageName>`

You can now use your own IaC templates or use one from `./samples` and call the API with the following parameters:

- framework: `<arm/cloudformatio>`
- file_type: `<json/yaml>`

The request body contains the full template string.

Example using cURL calling the live ARGOS API:

```curl
curl --location --request POST 'https://test-iac.argos-security.io/api/iac-test?provider=arm&file_type=json' \
--header 'Content-Type: application/json' \
--data-raw '{
  "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentTemplate.json#",
  "contentVersion": "1.0.0.0",
  "parameters": {
      "projectName": {
          "type": "string",
          "minLength": 1,
          "maxLength": 5,
          "metadata": {
              "description": "Define the project name or prefix for all objects."
          }
      },
      "adminUser": {
          "type": "string",
          "metadata": {
              "description": "What is the username for the admin on VMs and SQL Server?"
          }
      },
      "adminPasswd": {
          "type": "securestring",
          "metadata": {
              "description": "What is the password for the admin on VMs and SQL Server?"
          }
      },        
      "location": {
          "type": "string",
          "defaultValue": "[resourceGroup().location]",
          "metadata": {
              "description": "The location for resources on template. By default, the same as resource group location."
          }
      },
      "timeZoneID": {
          "type": "string",
          "defaultValue": "UTC",
          "metadata": {
              "description": "TimeZone ID to be used on VMs. Get available timezones with powershell Get-TimeZone command."
          }
      },
      "externalDnsZone": {
          "type": "string",
          "defaultValue": "contosocorp.com",
          "metadata": {
              "description": "External public DNS domain zone. NOT AD domain. This the external domain your certs will point to."
          }
      },
      "deployHA": {
          "type": "bool",
          "defaultValue": false,
          "metadata": {
              "description": "This will trigger certificate request and HA deployment. If set to false, will not create HA deployment nor request certificates."
          }
      },
      "dcCount": {
          "type": "int",
          "defaultValue": 1,
          "metadata": {
              "description": "How many Domain Controllers would you like to deploy?"
          }            
      },        
      "rdcbCount": {
          "type": "int",
          "defaultValue": 1,
          "metadata": {
              "description": "How many RD Connection Brokers would you like to deploy?"
          }
      },
      "rdwgCount": {
          "type": "int",
          "defaultValue": 1,
          "metadata": {
              "description": "How many RD Web Access/Gateways would you like to deploy?"
          }            
      },
      "rdshCount": {
          "type": "int",
          "defaultValue": 1,
          "metadata": {
              "description": "How many RD Session Hosts would you like to deploy?"
          }            
      },
      "lsfsCount": {
          "type": "int",
          "defaultValue": 1,
          "metadata": {
              "description": "How many License/File Servers would you like to deploy?"
          }            
      },
      "vmSize": {
          "type": "string",
          "defaultValue": "Standard_A2_v2",
          "allowedValues": [
              "Standard_A2_v2",
              "Standard_A4_v2",
              "Standard_A8_v2",
              "Standard_D1_v2",
              "Standard_D2_v2",
              "Standard_D3_v2",                
              "Standard_D2_v3",
              "Standard_D4_v3",
              "Standard_DS1_v2",
              "Standard_DS2_v2"
          ],
          "metadata": {
              "description": "What is the VM size for all VMs?"
          }            
      },
      "vmSpot": {
          "type": "bool",
          "defaultValue": true,
          "metadata": {
              "description": "Create Azure Spot VMs?"
          }
      },
      "vmStorageSkuType": {
          "type": "string",
          "defaultValue": "Standard_LRS",
          "allowedValues": [
              "StandardSSD_LRS",
              "Standard_LRS"
          ],
          "metadata": {
              "description": "What is the SKU for the storage to VM managed disks?"
          }            
      },
      "adDomainName": {
          "type": "string",
          "defaultValue": "contoso.com",
          "metadata": {
              "description": "What is the new forest/root Active Directory domain name?"
          }            
      },
      "vNetPrefix": {
          "type": "string",
          "defaultValue": "10.100",
          "metadata": {
              "description": "What is the prefix for the vnet and first subnet?"
          }            
      },
      "vNetAddressSpace": {
          "type": "string",
          "defaultValue": "[concat(parameters('\''vNetPrefix'\''),'\''.0.0/16'\'')]",
          "metadata": {
              "description": "What is the vnet address space?"
          }            
      },
      "vNetSubnetAddress": {
          "type": "string",
          "defaultValue": "[concat(parameters('\''vNetPrefix'\''),'\''.0.0/24'\'')]",
          "metadata": {
              "description": "What is the subnet address prefix?"
          }            
      },       
      "_artifactsLocation": {
          "type": "string",
          "defaultValue": "https://raw.githubusercontent.com/Azure/azure-quickstart-templates/master/101-rds-deployment-full-ha/",
          "metadata": {
              "description": "Location of all scripts and DSC resources for RDS deployment."
          }
      },
      "_artifactsLocationSasToken": {
          "type": "securestring",
          "defaultValue": "",
          "metadata": {
              "description": "SAS storage token to access _artifactsLocation. No need to change unless you copy or fork this template."
          }
      }
  },
  "variables": {
      "uniqueName": "[substring(uniqueString(resourceGroup().id,deployment().name),0,5)]",
      "dnsEntry": "remoteapps",
      "brokerName": "broker",
      "externalFqdn": "[concat(variables('\''dnsEntry'\''),'\''.'\'',toLower(parameters('\''externalDnsZone'\'')))]",
      "brokerFqdn": "[concat(variables('\''brokerName'\''),'\''.'\'',toLower(parameters('\''externalDnsZone'\'')))]",
      "vmNames": [
          "[concat(toLower(parameters('\''projectName'\'')),variables('\''uniqueName'\''),'\''dc'\'')]",
          "[concat(toLower(parameters('\''projectName'\'')),variables('\''uniqueName'\''),'\''wg'\'')]",
          "[concat(toLower(parameters('\''projectName'\'')),variables('\''uniqueName'\''),'\''cb'\'')]",
          "[concat(toLower(parameters('\''projectName'\'')),variables('\''uniqueName'\''),'\''sh'\'')]",
          "[concat(toLower(parameters('\''projectName'\'')),variables('\''uniqueName'\''),'\''lf'\'')]"
      ],
      "vmProperties": [
          {
              "name": "[variables('\''vmNames'\'')[0]]",
              "count": "[parameters('\''dcCount'\'')]",
              "intLbBackEndPool": "",
              "pubLbBackEndPool": "",
              "dscFunction": "DeployRDSLab.ps1\\CreateRootDomain"
          },                
          {
              "name": "[variables('\''vmNames'\'')[1]]",
              "count": "[parameters('\''rdwgCount'\'')]",
              "intLbBackEndPool": "rds-webgateways-int-pool",
              "pubLbBackEndPool": "rds-webgateways-pub-pool",
              "dscFunction": "DeployRDSLab.ps1\\RDWebGateway"
          },
          {
              "name": "[variables('\''vmNames'\'')[2]]",
              "count": "[parameters('\''rdcbCount'\'')]",
              "intLbBackEndPool": "rds-brokers-int-pool",
              "pubLbBackEndPool": "",
              "dscFunction": "DeployRDSLab.ps1\\RDSDeployment"
          },
          {
              "name": "[variables('\''vmNames'\'')[3]]",
              "count": "[parameters('\''rdshCount'\'')]",
              "intLbBackEndPool": "",
              "pubLbBackEndPool": "",
              "dscFunction": "DeployRDSLab.ps1\\RDSessionHost"
          },
          {
              "name": "[variables('\''vmNames'\'')[4]]",
              "count": "[parameters('\''lsfsCount'\'')]",
              "intLbBackEndPool": "",
              "pubLbBackEndPool": "",
              "dscFunction": "DeployRDSLab.ps1\\RDLicenseServer"
          }                               
      ],
      "diagStorageName": "[concat(toLower(parameters('\''projectName'\'')),variables('\''uniqueName'\''),'\''diag'\'')]",
      "publicLbIpName": "[concat(toLower(parameters('\''projectName'\'')),'\''lbpip'\'')]",
      "diagStorageSkuType": "Standard_LRS",
      "vNetName": "[concat(parameters('\''projectName'\''),'\''vnet'\'')]",
      "firstDcIP": "[concat(parameters('\''vNetPrefix'\''),'\''.0.99'\'')]",
      "nsgRef": "[resourceId('\''Microsoft.Network/networkSecurityGroups'\'',concat(parameters('\''projectName'\''),'\''nsg'\''))]",
      "subNetRef": "[resourceId('\''Microsoft.Network/virtualNetworks/subnets'\'',variables('\''vNetName'\''),concat(parameters('\''projectName'\''),'\''main'\''))]",
      "sqlServerName": "[concat(toLower(parameters('\''projectName'\'')),variables('\''uniqueName'\''),'\''sql'\'')]",
      "rdsDBName": "rdsdb",
      "dscScriptName": "deployrdslab.zip",
      "scriptName": "deploycertha.ps1"
  },
  "resources": [
      {
          "type": "Microsoft.Storage/storageAccounts",
          "apiVersion": "2019-06-01",
          "location": "[parameters('\''location'\'')]",
          "kind": "StorageV2",
          "name": "[variables('\''diagStorageName'\'')]",
          "sku": {
              "name": "[variables('\''diagStorageSkuType'\'')]",
              "tier": "Standard"
          }
      },
      {
          "type": "Microsoft.Network/networkSecurityGroups",
          "apiVersion": "2019-12-01",
          "location": "[parameters('\''location'\'')]",
          "name": "[concat(parameters('\''projectName'\''),'\''nsg'\'')]",
          "properties": {
              "securityRules": [
                  {
                      "name": "Allow_RDP",
                      "properties": {
                          "access": "Allow",
                          "sourceAddressPrefix": "*",
                          "sourcePortRange": "*",
                          "destinationAddressPrefix": "*",
                          "destinationPortRange": "3389",
                          "protocol": "*",
                          "direction": "Inbound",
                          "priority": 1000
                      }
                  },
                  {
                      "name": "Allow_HTTP",
                      "properties": {
                          "access": "Allow",
                          "sourceAddressPrefix": "*",
                          "sourcePortRange": "*",
                          "destinationAddressPrefix": "*",
                          "destinationPortRange": "80",
                          "protocol": "Tcp",
                          "direction": "Inbound",
                          "priority": 1001                            
                      }
                  },
                  {
                      "name": "Allow_HTTPS",
                      "properties": {
                          "access": "Allow",
                          "sourceAddressPrefix": "*",
                          "sourcePortRange": "*",
                          "destinationAddressPrefix": "*",
                          "destinationPortRange": "443",
                          "protocol": "Tcp",
                          "direction": "Inbound",
                          "priority": 1002                        
                      }
                  },
                  {
                      "name": "Allow_UDP_3391",
                      "properties": {
                          "access": "Allow",
                          "sourceAddressPrefix": "*",
                          "sourcePortRange": "*",
                          "destinationAddressPrefix": "*",
                          "destinationPortRange": "3391",
                          "protocol": "Udp",
                          "direction": "Inbound",
                          "priority": 1003                        
                      }
                  }                                     
              ]
          }
      },
      {
          "type": "Microsoft.Network/virtualNetworks",
          "apiVersion": "2019-12-01",
          "location": "[parameters('\''location'\'')]",
          "name": "[concat(parameters('\''projectName'\''),'\''vnet'\'')]",
          "dependsOn": [
              "[variables('\''nsgRef'\'')]"
          ],
          "properties": {
              "addressSpace": {
                  "addressPrefixes": [
                      "[parameters('\''vNetAddressSpace'\'')]"
                  ]
              },
              "subnets": [
                  {
                      "name": "[concat(parameters('\''projectName'\''),'\''main'\'')]",
                      "properties": {
                          "addressPrefix": "[parameters('\''vNetSubnetAddress'\'')]",
                          "networkSecurityGroup": {
                              "id": "[variables('\''nsgRef'\'')]"
                          }
                      }
                  }
              ]
          }
      },
      {
          "type": "Microsoft.Network/loadBalancers",
          "apiVersion": "2019-12-01",
          "location": "[parameters('\''location'\'')]",
          "name": "[concat(parameters('\''projectName'\''),'\''intlb'\'')]",
          "sku": {
              "name": "Standard"
          },
          "dependsOn": [
              "[resourceId('\''Microsoft.Network/virtualNetworks'\'',concat(parameters('\''projectName'\''),'\''vnet'\''))]"
          ],
          "properties": {
              "frontendIPConfigurations": [
                  {
                      "name": "rds-brokers-frontend",
                      "properties": {
                          "privateIPAllocationMethod": "Static",
                          "privateIPAddress": "[concat(parameters('\''vNetPrefix'\''),'\''.0.4'\'')]",
                          "privateIPAddressVersion": "IPv4",
                          "subnet": {
                              "id": "[variables('\''subNetRef'\'')]"
                          }
                      }
                  },
                  {
                      "name": "rds-webgateways-frontend",
                      "properties": {
                          "privateIPAllocationMethod": "Dynamic",
                          "privateIPAddressVersion": "IPv4",
                          "subnet": {
                              "id": "[variables('\''subNetRef'\'')]"
                          }
                      }
                  }
              ],
              "backendAddressPools": [
                  {
                      "name": "rds-brokers-int-pool",
                      "properties": {
                      }
                  },
                  {
                      "name": "rds-webgateways-int-pool",
                      "properties": {
                      }                
                  }
              ],
              "probes": [
                  {
                      "name": "rds-broker-probe",
                      "properties": {
                          "intervalInSeconds": 5,
                          "numberOfProbes": 2,
                          "protocol": "Tcp",
                          "port": 3389
                      }
                  },
                  {
                      "name": "rds-webgateway-probe",
                      "properties": {
                          "intervalInSeconds": 5,
                          "numberOfProbes": 2,
                          "protocol": "Tcp",
                          "port": 443
                      }
                  }
              ],
              "loadBalancingRules": [
                  {
                      "name": "rds-brokers-tcp-rule",
                      "properties": {
                          "frontendIPConfiguration": {
                              "id": "[resourceId('\''Microsoft.Network/loadBalancers/frontendIpConfigurations'\'',concat(parameters('\''projectName'\''),'\''intlb'\''),'\''rds-brokers-frontend'\'')]"
                          },
                          "backendAddressPool": {
                              "id": "[resourceId('\''Microsoft.Network/loadBalancers/backendAddressPools'\'',concat(parameters('\''projectName'\''),'\''intlb'\''),'\''rds-brokers-int-pool'\'')]"
                          },
                          "probe": {
                              "id": "[resourceId('\''Microsoft.Network/loadBalancers/probes'\'',concat(parameters('\''projectName'\''),'\''intlb'\''),'\''rds-broker-probe'\'')]"
                          },
                          "protocol": "Tcp",
                          "frontendPort": 3389,
                          "backendPort": 3389,
                          "idleTimeoutInMinutes": 4
                      }
                  },
                  {
                      "name": "rds-brokers-udp-rule",
                      "properties": {
                          "frontendIPConfiguration": {
                              "id": "[resourceId('\''Microsoft.Network/loadBalancers/frontendIpConfigurations'\'',concat(parameters('\''projectName'\''),'\''intlb'\''),'\''rds-brokers-frontend'\'')]"
                          },
                          "backendAddressPool": {
                              "id": "[resourceId('\''Microsoft.Network/loadBalancers/backendAddressPools'\'',concat(parameters('\''projectName'\''),'\''intlb'\''),'\''rds-brokers-int-pool'\'')]"
                          },
                          "probe": {
                              "id": "[resourceId('\''Microsoft.Network/loadBalancers/probes'\'',concat(parameters('\''projectName'\''),'\''intlb'\''),'\''rds-broker-probe'\'')]"
                          },
                          "protocol": "Udp",
                          "frontendPort": 3389,
                          "backendPort": 3389,
                          "idleTimeoutInMinutes": 4
                      }
                  },                    
                  {
                      "name": "rds-webgateway-http-rule",
                      "properties": {
                          "frontendIPConfiguration": {
                              "id": "[resourceId('\''Microsoft.Network/loadBalancers/frontendIpConfigurations'\'',concat(parameters('\''projectName'\''),'\''intlb'\''),'\''rds-webgateways-frontend'\'')]"
                          },
                          "backendAddressPool": {
                              "id": "[resourceId('\''Microsoft.Network/loadBalancers/backendAddressPools'\'',concat(parameters('\''projectName'\''),'\''intlb'\''),'\''rds-webgateways-int-pool'\'')]"
                          },
                          "probe": {
                              "id": "[resourceId('\''Microsoft.Network/loadBalancers/probes'\'',concat(parameters('\''projectName'\''),'\''intlb'\''),'\''rds-webgateway-probe'\'')]"
                          },
                          "protocol": "Tcp",
                          "frontendPort": 80,
                          "backendPort": 80,
                          "idleTimeoutInMinutes": 4
                      }                      
                  },
                  {
                      "name": "rds-webgateway-https-rule",
                      "properties": {
                          "frontendIPConfiguration": {
                              "id": "[resourceId('\''Microsoft.Network/loadBalancers/frontendIpConfigurations'\'',concat(parameters('\''projectName'\''),'\''intlb'\''),'\''rds-webgateways-frontend'\'')]"
                          },
                          "backendAddressPool": {
                              "id": "[resourceId('\''Microsoft.Network/loadBalancers/backendAddressPools'\'',concat(parameters('\''projectName'\''),'\''intlb'\''),'\''rds-webgateways-int-pool'\'')]"
                          },
                          "probe": {
                              "id": "[resourceId('\''Microsoft.Network/loadBalancers/probes'\'',concat(parameters('\''projectName'\''),'\''intlb'\''),'\''rds-webgateway-probe'\'')]"
                          },
                          "protocol": "Tcp",
                          "frontendPort": 443,
                          "backendPort": 443,
                          "idleTimeoutInMinutes": 4
                      }                      
                  },
                  {
                      "name": "rds-webgateway-udp-rule",
                      "properties": {
                          "frontendIPConfiguration": {
                              "id": "[resourceId('\''Microsoft.Network/loadBalancers/frontendIpConfigurations'\'',concat(parameters('\''projectName'\''),'\''intlb'\''),'\''rds-webgateways-frontend'\'')]"
                          },
                          "backendAddressPool": {
                              "id": "[resourceId('\''Microsoft.Network/loadBalancers/backendAddressPools'\'',concat(parameters('\''projectName'\''),'\''intlb'\''),'\''rds-webgateways-int-pool'\'')]"
                          },
                          "probe": {
                              "id": "[resourceId('\''Microsoft.Network/loadBalancers/probes'\'',concat(parameters('\''projectName'\''),'\''intlb'\''),'\''rds-webgateway-probe'\'')]"
                          },
                          "protocol": "Udp",
                          "frontendPort": 3391,
                          "backendPort": 3391,
                          "idleTimeoutInMinutes": 4
                      }                      
                  }                                      
              ]
          }
      },
      {
          "name": "[variables('\''publicLbIpName'\'')]",
          "type": "Microsoft.Network/publicIPAddresses",
          "apiVersion": "2019-11-01",
          "location": "[parameters('\''location'\'')]",
          "sku": {
              "name": "Standard"
          },
          "properties": {
              "publicIPAllocationMethod": "Static",
              "dnsSettings": {
                  "domainNameLabel": "[variables('\''publicLbIpName'\'')]"
              }
          }
      },
      {
          "name": "[concat(parameters('\''projectName'\''),'\''publb'\'')]",
          "type": "Microsoft.Network/loadBalancers",
          "apiVersion": "2019-11-01",
          "location": "[parameters('\''location'\'')]",
          "dependsOn": [
              "[resourceId('\''Microsoft.Network/publicIPAddresses'\'',variables('\''publicLbIpName'\''))]",
              "[resourceId('\''Microsoft.Network/virtualNetworks'\'',concat(parameters('\''projectName'\''),'\''vnet'\''))]"
          ],
          "sku": {
              "name": "Standard"
          },
          "properties": {
              "frontendIPConfigurations": [
                  {
                      "name": "rds-webgateways-frontend",
                      "properties": {
                          "publicIPAddress": {
                              "id": "[resourceId('\''Microsoft.Network/publicIPAddresses'\'',variables('\''publicLbIpName'\''))]"
                          }
                      }
                  }
              ],
              "backendAddressPools": [
                  {
                      "name": "rds-webgateways-pub-pool"
                  }
              ],
              "probes": [
                  {
                      "name": "rds-webgateways-probe",
                      "properties": {
                          "protocol": "Tcp",
                          "port": 80,
                          "intervalInSeconds": 5,
                          "numberOfProbes": 2
                      }
                  }
              ],                
              "loadBalancingRules": [
                  {
                      "name": "rds-webgateways-http-rule",
                      "properties": {
                          "frontendIPConfiguration": {
                              "id": "[resourceId('\''Microsoft.Network/loadBalancers/frontendIPConfigurations'\'',concat(parameters('\''projectName'\''),'\''publb'\''),'\''rds-webgateways-frontend'\'')]"
                          },
                          "backendAddressPool": {
                              "id": "[resourceId('\''Microsoft.Network/loadBalancers/backendAddressPools'\'',concat(parameters('\''projectName'\''),'\''publb'\''),'\''rds-webgateways-pub-pool'\'')]"
                          },
                          "probe": {
                              "id": "[resourceId('\''Microsoft.Network/loadBalancers/probes'\'',concat(parameters('\''projectName'\''),'\''publb'\''),'\''rds-webgateways-probe'\'')]"
                          },
                          "protocol": "Tcp",
                          "frontendPort": 80,
                          "backendPort": 80,
                          "enableFloatingIP": false,
                          "idleTimeoutInMinutes": 5                            
                      }
                  },
                  {
                      "name": "rds-webgateways-https-rule",
                      "properties": {
                          "frontendIPConfiguration": {
                              "id": "[resourceId('\''Microsoft.Network/loadBalancers/frontendIPConfigurations'\'',concat(parameters('\''projectName'\''),'\''publb'\''),'\''rds-webgateways-frontend'\'')]"
                          },
                          "backendAddressPool": {
                              "id": "[resourceId('\''Microsoft.Network/loadBalancers/backendAddressPools'\'',concat(parameters('\''projectName'\''),'\''publb'\''),'\''rds-webgateways-pub-pool'\'')]"
                          },
                          "probe": {
                              "id": "[resourceId('\''Microsoft.Network/loadBalancers/probes'\'',concat(parameters('\''projectName'\''),'\''publb'\''),'\''rds-webgateways-probe'\'')]"
                          },
                          "protocol": "Tcp",
                          "frontendPort": 443,
                          "backendPort": 443,
                          "enableFloatingIP": false,
                          "idleTimeoutInMinutes": 5                            
                      }
                  },
                  {
                      "name": "rds-webgateways-udp-rule",
                      "properties": {
                          "frontendIPConfiguration": {
                              "id": "[resourceId('\''Microsoft.Network/loadBalancers/frontendIPConfigurations'\'',concat(parameters('\''projectName'\''),'\''publb'\''),'\''rds-webgateways-frontend'\'')]"
                          },
                          "backendAddressPool": {
                              "id": "[resourceId('\''Microsoft.Network/loadBalancers/backendAddressPools'\'',concat(parameters('\''projectName'\''),'\''publb'\''),'\''rds-webgateways-pub-pool'\'')]"
                          },
                          "probe": {
                              "id": "[resourceId('\''Microsoft.Network/loadBalancers/probes'\'',concat(parameters('\''projectName'\''),'\''publb'\''),'\''rds-webgateways-probe'\'')]"
                          },
                          "protocol": "Udp",
                          "frontendPort": 3391,
                          "backendPort": 3391,
                          "enableFloatingIP": false,
                          "idleTimeoutInMinutes": 5                            
                      }
                  }                                        
              ]
          }
      },
      {
          "name": "[variables('\''sqlServerName'\'')]",
          "type": "Microsoft.Sql/servers",
          "apiVersion": "2019-06-01-preview",
          "location": "[parameters('\''location'\'')]",
          "properties": {
              "administratorLogin": "[parameters('\''adminUser'\'')]",
              "administratorLoginPassword": "[parameters('\''adminPasswd'\'')]"
          },
          "resources": [
              {
                  "type": "firewallRules",
                  "apiVersion": "2019-06-01-preview",
                  "dependsOn": [
                      "[resourceId('\''Microsoft.Sql/servers'\'',variables('\''sqlServerName'\''))]"
                  ],
                  "location": "[parameters('\''location'\'')]",
                  "name": "AllowAllWindowsAzureIps",
                  "properties": {
                      "startIpAddress": "0.0.0.0",
                      "endIpAddress": "0.0.0.0"
                  }
              }
          ]
      },
      {
          "name": "[concat(variables('\''sqlServerName'\''),'\''/'\'',variables('\''rdsDBName'\''))]",
          "type": "Microsoft.Sql/servers/databases",
          "apiVersion": "2019-06-01-preview",
          "location": "[parameters('\''location'\'')]",
          "dependsOn": [
              "[resourceId('\''Microsoft.Sql/servers'\'',variables('\''sqlServerName'\''))]"
          ],
          "properties": {
              "collation": "SQL_Latin1_General_CP1_CI_AS",
              "edition": "Basic",
              "maxSizeBytes": "1073741824",
              "requestedServiceObjectiveName": "Basic"
          }
      },
      {
          "type": "Microsoft.Resources/deployments",
          "apiVersion": "2019-10-01",
          "name": "[concat(variables('\''vmProperties'\'')[copyIndex()].name,'\''Deployment'\'')]",
          "copy": {
              "name": "vmCopy",
              "count": "[length(variables('\''vmProperties'\''))]"
          },            
          "dependsOn": [
              "[resourceId('\''Microsoft.Network/virtualNetworks'\'',concat(parameters('\''projectName'\''),'\''vnet'\''))]",
              "[resourceId('\''Microsoft.Network/loadBalancers'\'',concat(parameters('\''projectName'\''),'\''intlb'\''))]",
              "[resourceId('\''Microsoft.Network/loadBalancers'\'',concat(parameters('\''projectName'\''),'\''publb'\''))]",
              "[resourceId('\''Microsoft.Storage/storageAccounts'\'',variables('\''diagStorageName'\''))]",
              "[resourceId('\''Microsoft.Sql/servers/databases'\'',variables('\''sqlServerName'\''),variables('\''rdsDBName'\''))]"
          ],
          "properties": {
              "mode": "Incremental",
              "expressionEvaluationOptions": {
                  "scope": "inner"
              },
              "parameters": {
                  "projectName": {
                      "value": "[parameters('\''projectName'\'')]"
                  },
                  "location": {
                      "value": "[parameters('\''location'\'')]"
                  },
                  "timeZoneID": {
                      "value": "[parameters('\''timeZoneID'\'')]"
                  },
                  "loopCount": {
                      "value": "[variables('\''vmProperties'\'')[copyIndex()].count]"
                  },
                  "storageDiagUrl": {
                      "value": "[reference(resourceId('\''Microsoft.Storage/storageAccounts'\'',variables('\''diagStorageName'\''))).primaryEndpoints.blob]"
                  },
                  "vmName": {
                      "value": "[variables('\''vmProperties'\'')[copyIndex()].name]"
                  },
                  "subNetRef": {
                      "value": "[variables('\''subNetRef'\'')]"
                  },
                  "vmSize": {
                      "value": "[parameters('\''vmSize'\'')]"
                  },
                  "vmSpot": {
                      "value": "[parameters('\''vmSpot'\'')]"
                  },
                  "vmStorageSkuType": {
                      "value": "[parameters('\''vmStorageSkuType'\'')]"
                  },
                  "adminUser": {
                      "value": "[parameters('\''adminUser'\'')]"
                  },
                  "adminPasswd": {
                      "value": "[parameters('\''adminPasswd'\'')]"
                  },
                  "intLbName": {
                      "value": "[concat(parameters('\''projectName'\''),'\''intlb'\'')]"
                  },
                  "intLbBackEndPool": {
                      "value": "[variables('\''vmProperties'\'')[copyIndex()].intLbBackEndPool]"
                  },
                  "intLbBrokerIP": {
                      "value": "[reference(resourceId('\''Microsoft.Network/loadBalancers'\'',concat(parameters('\''projectName'\''),'\''intlb'\''))).frontendIPConfigurations[0].properties.privateIPAddress]"
                  },
                  "intLbWebGWIP": {
                      "value": "[reference(resourceId('\''Microsoft.Network/loadBalancers'\'',concat(parameters('\''projectName'\''),'\''intlb'\''))).frontendIPConfigurations[1].properties.privateIPAddress]"
                  },                    
                  "pubLbName": {
                      "value": "[concat(parameters('\''projectName'\''),'\''publb'\'')]"
                  },
                  "pubLbBackEndPool": {
                      "value": "[variables('\''vmProperties'\'')[copyIndex()].pubLbBackEndPool]"
                  },
                  "adDomainName": {
                      "value": "[parameters('\''adDomainName'\'')]"
                  },
                  "firstDcIP": {
                      "value": "[variables('\''firstDcIP'\'')]"
                  },
                  "dcName": {
                      "value": "[variables('\''vmProperties'\'')[0].name]"
                  },                   
                  "MainConnectionBroker": {
                      "value": "[concat(variables('\''vmProperties'\'')[2].name,'\''1'\'')]"
                  },
                  "WebAccessServerName": {
                      "value": "[variables('\''vmProperties'\'')[1].name]"
                  },
                  "WebAccessServerCount": {
                      "value": "[variables('\''vmProperties'\'')[1].count]"
                  },
                  "SessionHostName": {
                      "value": "[variables('\''vmProperties'\'')[3].name]"
                  },
                  "SessionHostCount": {
                      "value": "[variables('\''vmProperties'\'')[3].count]"
                  },                    
                  "LicenseServerName": {
                      "value": "[variables('\''vmProperties'\'')[4].name]"
                  },
                  "LicenseServerCount": {
                      "value": "[variables('\''vmProperties'\'')[4].count]"
                  },
                  "externalFqdn": {
                      "value": "[variables('\''externalFqdn'\'')]"
                  },
                  "brokerFqdn": {
                      "value": "[variables('\''brokerFqdn'\'')]"
                  },
                  "externalDnsZone": {
                      "value": "[parameters('\''externalDnsZone'\'')]"
                  },                    
                  "dscFunction": {
                      "value": "[variables('\''vmProperties'\'')[copyIndex()].dscFunction]"
                  },
                  "dscLocation": {
                      "value": "[parameters('\''_artifactsLocation'\'')]"
                  },
                  "dscScriptName": {
                      "value": "[variables('\''dscScriptName'\'')]"
                  },
                  "scriptName": {
                      "value": "[variables('\''scriptName'\'')]"
                  },
                  "deployHA": {
                      "value": "[parameters('\''deployHA'\'')]"
                  },
                  "rdsDBName": {
                      "value": "[variables('\''rdsDBName'\'')]"
                  },
                  "azureSqlFqdn": {
                      "value": "[reference(resourceId('\''Microsoft.Sql/servers'\'',variables('\''sqlServerName'\''))).fullyQualifiedDomainName]"
                  },
                  "webGwName": {
                      "value": "[variables('\''dnsEntry'\'')]"
                  },
                  "_artifactsLocationSasToken": {
                      "value": "[parameters('\''_artifactsLocationSasToken'\'')]"
                  }
              },
              "template": {
                  "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentTemplate.json#",
                  "contentVersion": "1.0.0.0",
                  "parameters": {
                      "projectName": {
                          "type": "string"
                      },
                      "location": {
                          "type": "string"
                      },
                      "timeZoneID": {
                          "type": "string"
                      },
                      "loopCount": {
                          "type": "int"
                      },
                      "storageDiagUrl": {
                          "type": "string"
                      },
                      "vmName": {
                          "type": "string"
                      },
                      "subNetRef": {
                          "type": "string"
                      },
                      "vmSize": {
                          "type": "string"
                      },
                      "vmSpot": {
                          "type": "bool"
                      },
                      "vmStorageSkuType": {
                          "type": "string"
                      },
                      "adminUser": {
                          "type": "string"
                      },
                      "adminPasswd": {
                          "type": "securestring"
                      },
                      "intLbName": {
                          "type": "string"
                      },
                      "intLbBackEndPool": {
                          "type": "string"
                      },
                      "intLbBrokerIP": {
                          "type": "string"
                      },
                      "intLbWebGWIP": {
                          "type": "string"
                      },
                      "pubLbName": {
                          "type": "string"
                      },
                      "pubLbBackEndPool": {
                          "type": "string"
                      },
                      "adDomainName": {
                          "type": "string"
                      },
                      "firstDcIP": {
                          "type": "string"
                      },
                      "dcName": {
                          "type": "string"
                      },
                      "MainConnectionBroker": {
                          "type": "string"
                      },
                      "WebAccessServerName": {
                          "type": "string"
                      },
                      "WebAccessServerCount": {
                          "type": "int"
                      },
                      "SessionHostName": {
                          "type": "string"
                      },
                      "SessionHostCount": {
                          "type": "int"
                      },
                      "LicenseServerName": {
                          "type": "string"
                      },
                      "LicenseServerCount": {
                          "type": "int"
                      },
                      "externalFqdn": {
                          "type": "string"
                      },
                      "brokerFqdn": {
                          "type": "string"
                      },
                      "externalDnsZone": {
                          "type": "string"
                      },                                                                                                                                                                  
                      "dscFunction": {
                          "type": "string"
                      },
                      "dscLocation": {
                          "type": "string"
                      },
                      "dscScriptName": {
                          "type": "string"
                      },
                      "scriptName": {
                          "type": "string"
                      },
                      "deployHA": {
                          "type": "bool"
                      },                      
                      "rdsDBName": {
                          "type": "string"
                      },
                      "azureSQLFqdn": {
                          "type": "string"
                      },
                      "webGwName": {
                          "type": "string"
                      },
                      "_artifactsLocationSasToken": {
                          "type": "securestring"
                      }
                  },
                  "variables": {
                      "scriptPath": "[uri(parameters('\''dscLocation'\''),concat('\''scripts/'\'',parameters('\''scriptName'\''),parameters('\''_artifactsLocationSasToken'\'')))]",
                      "intlbPool": [
                          {
                              "id": "[resourceId('\''Microsoft.Network/loadBalancers/backendAddressPools'\'',parameters('\''intLbName'\''),parameters('\''intLbBackEndPool'\''))]"
                          }
                      ],
                      "pubIntlbPool": [
                          {
                              "id": "[resourceId('\''Microsoft.Network/loadBalancers/backendAddressPools'\'',parameters('\''intLbName'\''),parameters('\''intLbBackEndPool'\''))]"
                          },
                          {
                              "id": "[resourceId('\''Microsoft.Network/loadBalancers/backendAddressPools'\'',parameters('\''pubLbName'\''),parameters('\''pubLbBackEndPool'\''))]"
                          }                            
                      ],
                      "intlbRef": "[resourceId(parameters('\''location'\''),'\''Microsoft.Network/loadBalancers'\'',parameters('\''intLbName'\''))]"
                  },
                  "resources": [
                      {
                          "type": "Microsoft.Network/publicIPAddresses",
                          "apiVersion": "2019-12-01",
                          "name": "[concat(parameters('\''vmName'\''),copyIndex(1),'\''pip'\'')]",
                          "location": "[parameters('\''location'\'')]",
                          "sku": {
                              "name": "Standard"
                          },
                          "copy": {
                              "name": "[concat(parameters('\''vmName'\''),'\''pipcopy'\'')]",
                              "count": "[parameters('\''loopCount'\'')]"
                          },                            
                          "properties": {
                              "publicIPAllocationMethod": "Static",
                              "dnsSettings": {
                                  "domainNameLabel": "[concat(parameters('\''vmName'\''),'\''pip'\'',copyIndex(1))]"
                              }
                          }
                      },
                      {
                          "type": "Microsoft.Network/networkInterfaces",
                          "apiVersion": "2019-12-01",
                          "location": "[parameters('\''location'\'')]",
                          "name": "[concat(parameters('\''vmName'\''),copyIndex(1),'\''nic1'\'')]",
                          "copy": {
                              "name": "[concat(parameters('\''vmName'\''),'\''niccopy'\'')]",
                              "count": "[parameters('\''loopCount'\'')]"
                          },                            
                          "dependsOn": [
                              "[resourceId('\''Microsoft.Network/publicIPAddresses'\'',concat(parameters('\''vmName'\''),copyIndex(1),'\''pip'\''))]"
                          ],                          
                          "properties": {
                              "ipConfigurations": [
                                  {
                                      "name": "ipconfig",
                                      "properties": {
                                          "subnet": {
                                              "id": "[parameters('\''subNetRef'\'')]"
                                          },
                                          "privateIPAllocationMethod": "[if(equals(parameters('\''vmName'\''),parameters('\''dcName'\'')),if(equals(copyIndex(1),1),'\''static'\'','\''dynamic'\''),'\''dynamic'\'')]",
                                          "privateIPAddress": "[if(equals(parameters('\''vmName'\''),parameters('\''dcName'\'')),if(equals(copyIndex(1),1),parameters('\''firstDcIP'\''),json('\''null'\'')),json('\''null'\''))]",
                                          "publicIPAddress": {
                                              "id": "[resourceId('\''Microsoft.Network/publicIPAddresses'\'',concat(parameters('\''vmName'\''),copyIndex(1),'\''pip'\''))]"
                                          },
                                          "loadBalancerBackendAddressPools": "[if(not(empty(parameters('\''intLbBackEndPool'\''))),if(not(empty(parameters('\''pubLbBackEndPool'\''))),variables('\''pubIntlbPool'\''),variables('\''intlbPool'\'')),json('\''null'\''))]"
                                      }
                                  }
                              ]
                          }                                                        
                      },
                      {
                          "type": "Microsoft.Compute/virtualMachines",
                          "apiVersion": "2019-07-01",
                          "name": "[concat(parameters('\''vmName'\''),copyIndex(1))]",                             
                          "location": "[parameters('\''location'\'')]",
                          "copy": {
                              "name": "[concat(parameters('\''vmName'\''),'\''vmcopy'\'')]",
                              "count": "[parameters('\''loopCount'\'')]"                                
                          },                          
                          "dependsOn": [
                              "[resourceId('\''Microsoft.Network/networkInterfaces'\'',concat(parameters('\''vmName'\''),copyIndex(1),'\''nic1'\''))]"
                          ],
                          "properties": {
                              "licenseType": "Windows_Server",
                              "billingProfile": {
                                  "maxPrice": "[if(equals(parameters('\''vmSpot'\''),bool('\''true'\'')),'\''-1'\'',json('\''null'\''))]"
                              },
                              "priority": "[if(equals(parameters('\''vmSpot'\''),bool('\''true'\'')),'\''Spot'\'',json('\''null'\''))]",
                              "evictionPolicy": "[if(equals(parameters('\''vmSpot'\''),bool('\''true'\'')),'\''Deallocate'\'',json('\''null'\''))]",
                              "diagnosticsProfile": {
                                  "bootDiagnostics": {
                                      "enabled": true,
                                      "storageUri": "[parameters('\''storageDiagUrl'\'')]"
                                  }
                              },
                              "networkProfile": {
                                  "networkInterfaces": [
                                      {
                                          "id": "[resourceId('\''Microsoft.Network/networkInterfaces'\'',concat(parameters('\''vmName'\''),copyIndex(1),'\''nic1'\''))]"
                                      }
                                  ]
                              },
                              "osProfile": {
                                  "adminUsername": "[parameters('\''adminUser'\'')]",
                                  "adminPassword": "[parameters('\''adminPasswd'\'')]",
                                  "computerName": "[concat(parameters('\''vmName'\''),copyIndex(1))]"
                              },
                              "hardwareProfile": {
                                  "vmSize": "[parameters('\''vmSize'\'')]"
                              },
                              "storageProfile": {
                                  "osDisk": {
                                      "createOption": "FromImage",
                                      "managedDisk": {
                                          "storageAccountType": "[parameters('\''vmStorageSkuType'\'')]"
                                      }
                                  },
                                  "imageReference": {
                                      "publisher": "MicrosoftWindowsServer",
                                      "offer": "WindowsServer",
                                      "sku": "2019-Datacenter",
                                      "version": "latest"
                                  }
                              }
                          },
                          "resources": [
                              {
                                  "type": "Microsoft.Compute/virtualMachines/extensions",
                                  "apiVersion": "2019-12-01",
                                  "name": "[concat(parameters('\''vmName'\''),copyIndex(1),'\''/dscext'\'')]",
                                  "location": "[parameters('\''location'\'')]",
                                  "condition": "[not(empty(parameters('\''dscFunction'\'')))]",
                                  "dependsOn": [
                                      "[resourceId('\''Microsoft.Compute/virtualMachines'\'',concat(parameters('\''vmName'\''),copyIndex(1)))]"
                                  ],
                                  "properties": {
                                      "publisher": "Microsoft.Powershell",
                                      "type": "DSC",
                                      "typeHandlerVersion": "2.11",
                                      "autoUpgradeMinorVersion": true,
                                      "settings": {
                                          "ModulesUrl": "[uri(parameters('\''dscLocation'\''),concat('\''dsc/'\'',parameters('\''dscScriptName'\''),parameters('\''_artifactsLocationSasToken'\'')))]",
                                          "ConfigurationFunction": "[parameters('\''dscFunction'\'')]",
                                          "Properties": {
                                              "AdminCreds": {
                                                  "UserName": "[parameters('\''adminUser'\'')]",
                                                  "Password": "PrivateSettingsRef:AdminPassword"
                                              },
                                              "RDSParameters": [
                                                  {
                                                      "timeZoneID": "[parameters('\''timeZoneID'\'')]",
                                                      "DomainName": "[parameters('\''adDomainName'\'')]",
                                                      "DNSServer": "[parameters('\''firstDcIP'\'')]",
                                                      "MainConnectionBroker": "[parameters('\''MainConnectionBroker'\'')]",
                                                      "WebAccessServer": "[concat(parameters('\''WebAccessServerName'\''),'\''1'\'')]",
                                                      "SessionHost": "[concat(parameters('\''SessionHostName'\''),'\''1'\'')]",
                                                      "LicenseServer": "[concat(parameters('\''LicenseServerName'\''),'\''1'\'')]",
                                                      "externalFqdn": "[parameters('\''externalFqdn'\'')]",
                                                      "externalDnsDomain": "[parameters('\''externalDnsZone'\'')]",                                                        
                                                      "IntBrokerLBIP": "[parameters('\''intLbBrokerIP'\'')]",
                                                      "IntWebGWLBIP": "[parameters('\''intLbWebGWIP'\'')]",
                                                      "WebGWDNS": "[parameters('\''webGwName'\'')]"
                                                  }
                                              ]
                                          }
                                      },
                                      "protectedSettings": {
                                          "Items": {
                                              "AdminPassword": "[parameters('\''adminPasswd'\'')]"
                                          }
                                      }                                                                  
                                  }
                              },
                              {
                                  "type": "Microsoft.Compute/virtualMachines/extensions",
                                  "apiVersion": "2019-12-01",
                                  "name": "[concat(parameters('\''vmName'\''),copyIndex(1),'\''/pwshext'\'')]",
                                  "location": "[parameters('\''location'\'')]",
                                  "condition": "[and(contains(parameters('\''vmName'\''),'\''cb'\''),parameters('\''deployHA'\''))]",
                                  "dependsOn": [
                                      "[resourceId('\''Microsoft.Compute/virtualMachines'\'',concat(parameters('\''vmName'\''),copyIndex(1)))]",
                                      "[resourceId('\''Microsoft.Compute/virtualMachines/extensions'\'',concat(parameters('\''vmName'\''),copyIndex(1)),'\''dscext'\'')]"
                                  ],
                                  "properties": {
                                      "publisher": "Microsoft.Compute",
                                      "type": "CustomScriptExtension",
                                      "typeHandlerVersion": "1.10",
                                      "autoUpgradeMinorVersion": true,
                                      "settings": {
                                          "fileUris": [
                                              "[variables('\''scriptPath'\'')]"
                                          ]
                                      },
                                      "protectedSettings": {
                                          "commandToExecute": "[concat('\''powershell -ExecutionPolicy Bypass -File ./'\'',parameters('\''scriptName'\''),'\'' -AdminUser '\'',parameters('\''adminUser'\''),'\'' -Passwd '\'',parameters('\''adminPasswd'\''),'\'' -MainConnectionBroker '\'',parameters('\''MainConnectionBroker'\''),'\'' -BrokerFqdn '\'',parameters('\''brokerFqdn'\''),'\'' -WebGatewayFqdn '\'',parameters('\''externalFqdn'\''),'\'' -AzureSQLFQDN '\'',parameters('\''azureSqlFqdn'\''),'\'' -AzureSQLDBName '\'',parameters('\''rdsDBName'\''),'\'' -WebAccessServerName '\'',parameters('\''WebAccessServerName'\''),'\'' -WebAccessServerCount '\'',parameters('\''WebAccessServerCount'\''),'\'' -SessionHostName '\'',parameters('\''SessionHostName'\''),'\'' -SessionHostCount '\'',parameters('\''SessionHostCount'\''),'\'' -LicenseServerName '\'',parameters('\''LicenseServerName'\''),'\'' -LicenseServerCount '\'',parameters('\''LicenseServerCount'\''))]"
                                      }
                                  }
                              }                                
                          ]              
                      }
                  ]
              }
          }           
      }
  ],
  "outputs": {
      "adminUser": {
          "type": "string",
          "value": "[parameters('\''adminUser'\'')]"
      },
      "WebAccessFQDN": {
          "type": "string",
          "value": "[reference(resourceId('\''Microsoft.Network/publicIPAddresses'\'',variables('\''publicLbIpName'\''))).dnsSettings.fqdn]"
      },
      "ExternalFQDN": {
          "type": "string",
          "value": "[variables('\''externalFqdn'\'')]",
          "condition": "[parameters('\''deployHA'\'')]"
      }        
  }
}'
```