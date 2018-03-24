$(document).ready(function(){
	var code = '0x606060405234156200001057600080fd5b60405162001031380380620010318339810160405280805182019190602001805182019190602001805190602001909190805182019190505033600460006101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff1602179055508360009080519060200190620000a292919062000106565b508060029080519060200190620000bb92919062000106565b508260019080519060200190620000d492919062000106565b5081600381905550600060068190555060006005819055506000600781905550600060088190555050505050620001b5565b828054600181600116156101000203166002900490600052602060002090601f016020900481019282601f106200014957805160ff19168380011785556200017a565b828001600101855582156200017a579182015b82811115620001795782518255916020019190600101906200015c565b5b5090506200018991906200018d565b5090565b620001b291905b80821115620001ae57600081600090555060010162000194565b5090565b90565b610e6c80620001c56000396000f3006060604052600436106100e6576000357c0100000000000000000000000000000000000000000000000000000000900463ffffffff16806306fdde03146100eb5780630fc4f5dc146101795780631a8adc24146101a25780631b9265b8146101db578063278ecde1146101f9578063534117e11461021c578063592dcaef1461024557806368df3abc1461026e5780638da5cb5b1461029757806398d5fdca146102ec578063a035b1fe14610315578063a2b40d191461033e578063b3f22a2f14610361578063b5cdaeba14610384578063ef430aa614610399578063f3ccaac014610427575b600080fd5b34156100f657600080fd5b6100fe6104b5565b6040518080602001828103825283818151815260200191508051906020019080838360005b8381101561013e578082015181840152602081019050610123565b50505050905090810190601f16801561016b5780820380516001836020036101000a031916815260200191505b509250505060405180910390f35b341561018457600080fd5b61018c610553565b6040518082815260200191505060405180910390f35b34156101ad57600080fd5b6101d9600480803573ffffffffffffffffffffffffffffffffffffffff1690602001909190505061055d565b005b6101e3610606565b6040518082815260200191505060405180910390f35b341561020457600080fd5b61021a600480803590602001909190505061078f565b005b341561022757600080fd5b61022f610983565b6040518082815260200191505060405180910390f35b341561025057600080fd5b61025861098d565b6040518082815260200191505060405180910390f35b341561027957600080fd5b610281610997565b6040518082815260200191505060405180910390f35b34156102a257600080fd5b6102aa6109a1565b604051808273ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200191505060405180910390f35b34156102f757600080fd5b6102ff6109c7565b6040518082815260200191505060405180910390f35b341561032057600080fd5b6103286109d1565b6040518082815260200191505060405180910390f35b341561034957600080fd5b61035f60048080359060200190919050506109d7565b005b341561036c57600080fd5b6103826004808035906020019091905050610a3d565b005b341561038f57600080fd5b610397610bf2565b005b34156103a457600080fd5b6103ac610cbc565b6040518080602001828103825283818151815260200191508051906020019080838360005b838110156103ec5780820151818401526020810190506103d1565b50505050905090810190601f1680156104195780820380516001836020036101000a031916815260200191505b509250505060405180910390f35b341561043257600080fd5b61043a610d5a565b6040518080602001828103825283818151815260200191508051906020019080838360005b8381101561047a57808201518184015260208101905061045f565b50505050905090810190601f1680156104a75780820380516001836020036101000a031916815260200191505b509250505060405180910390f35b60008054600181600116156101000203166002900480601f01602080910402602001604051908101604052809291908181526020018280546001816001161561010002031660029004801561054b5780601f106105205761010080835404028352916020019161054b565b820191906000526020600020905b81548152906001019060200180831161052e57829003601f168201915b505050505081565b6000600854905090565b600460009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff161415156105b957600080fd5b8073ffffffffffffffffffffffffffffffffffffffff166108fc6008549081150290604051600060405180830381858888f1935050505015156105fb57600080fd5b600060088190555050565b600080600354341015151561061a57600080fd5b6003543403905060016005540160058190555060a0604051908101604052803373ffffffffffffffffffffffffffffffffffffffff1681526020014281526020016000815260200160035481526020016000151581525060096000600554815260200190815260200160002060008201518160000160006101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff16021790555060208201518160010155604082015181600201556060820151816003015560808201518160040160006101000a81548160ff021916908315150217905550905050600354600a60006005548152602001908152602001600020819055506003546007600082825401925050819055506000811115610786573373ffffffffffffffffffffffffffffffffffffffff166108fc829081150290604051600060405180830381858888f19350505050151561078557600080fd5b5b60055491505090565b610797610df8565b600460009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff161415156107f357600080fd5b6009600083815260200190815260200160002060a060405190810160405290816000820160009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1681526020016001820154815260200160028201548152602001600382015481526020016004820160009054906101000a900460ff1615151515815250509050600a60008381526020019081526020016000206000905560096000838152602001908152602001600020600080820160006101000a81549073ffffffffffffffffffffffffffffffffffffffff02191690556001820160009055600282016000905560038201600090556004820160006101000a81549060ff021916905550508060600151600760008282540392505081905550806000015173ffffffffffffffffffffffffffffffffffffffff166108fc82606001519081150290604051600060405180830381858888f19350505050151561097f57600080fd5b5050565b6000600654905090565b6000600754905090565b6000600554905090565b600460009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1681565b6000600354905090565b60035481565b600460009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff16141515610a3357600080fd5b8060038190555050565b610a45610df8565b6009600083815260200190815260200160002060a060405190810160405290816000820160009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1681526020016001820154815260200160028201548152602001600382015481526020016004820160009054906101000a900460ff1615151515815250509050806000015173ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff16141515610b3357600080fd5b600a6000838152602001908152602001600020600090556064605e826060015102811515610b5d57fe5b0460066000828254019250508190555060646006826060015102811515610b8057fe5b04600860008282540192505081905550806060015160076000828254039250508190555060016009600084815260200190815260200160002060040160006101000a81548160ff0219169083151502179055504260096000848152602001908152602001600020600201819055505050565b600460009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff16141515610c4e57600080fd5b600460009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff166108fc6006549081150290604051600060405180830381858888f193505050501515610cb257600080fd5b6000600681905550565b60018054600181600116156101000203166002900480601f016020809104026020016040519081016040528092919081815260200182805460018160011615610100020316600290048015610d525780601f10610d2757610100808354040283529160200191610d52565b820191906000526020600020905b815481529060010190602001808311610d3557829003601f168201915b505050505081565b60028054600181600116156101000203166002900480601f016020809104026020016040519081016040528092919081815260200182805460018160011615610100020316600290048015610df05780601f10610dc557610100808354040283529160200191610df0565b820191906000526020600020905b815481529060010190602001808311610dd357829003601f168201915b505050505081565b60a060405190810160405280600073ffffffffffffffffffffffffffffffffffffffff16815260200160008152602001600081526020016000815260200160001515815250905600a165627a7a7230582038caa6edfdddcdb9757f3bddca8869f03b8c29fe811cd3475dbceab79e08d4650029';
	var abi = [
	{
		"constant": true,
		"inputs": [],
		"name": "owner",
		"outputs": [
			{
				"name": "",
				"type": "address"
			}
		],
		"payable": false,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": true,
		"inputs": [],
		"name": "category",
		"outputs": [
			{
				"name": "",
				"type": "string"
			}
		],
		"payable": false,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": true,
		"inputs": [],
		"name": "getPrice",
		"outputs": [
			{
				"name": "",
				"type": "uint256"
			}
		],
		"payable": false,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": true,
		"inputs": [],
		"name": "price",
		"outputs": [
			{
				"name": "",
				"type": "uint256"
			}
		],
		"payable": false,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": true,
		"inputs": [],
		"name": "getamount",
		"outputs": [
			{
				"name": "",
				"type": "uint256"
			}
		],
		"payable": false,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": true,
		"inputs": [],
		"name": "getamountHolded",
		"outputs": [
			{
				"name": "",
				"type": "uint256"
			}
		],
		"payable": false,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": true,
		"inputs": [],
		"name": "name",
		"outputs": [
			{
				"name": "",
				"type": "string"
			}
		],
		"payable": false,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": true,
		"inputs": [],
		"name": "getnalog",
		"outputs": [
			{
				"name": "",
				"type": "uint256"
			}
		],
		"payable": false,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": true,
		"inputs": [],
		"name": "getnumBuys",
		"outputs": [
			{
				"name": "",
				"type": "uint256"
			}
		],
		"payable": false,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": true,
		"inputs": [],
		"name": "image",
		"outputs": [
			{
				"name": "",
				"type": "string"
			}
		],
		"payable": false,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": false,
		"inputs": [
			{
				"name": "_order",
				"type": "uint256"
			}
		],
		"name": "approveReceived",
		"outputs": [],
		"payable": false,
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"constant": false,
		"inputs": [],
		"name": "transferOwnMoney",
		"outputs": [],
		"payable": false,
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"constant": false,
		"inputs": [
			{
				"name": "_new_price",
				"type": "uint256"
			}
		],
		"name": "changePrice",
		"outputs": [],
		"payable": false,
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"constant": false,
		"inputs": [
			{
				"name": "_order",
				"type": "uint256"
			}
		],
		"name": "refund",
		"outputs": [],
		"payable": false,
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"constant": false,
		"inputs": [
			{
				"name": "_nalogovaya",
				"type": "address"
			}
		],
		"name": "payNalog",
		"outputs": [],
		"payable": false,
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"constant": false,
		"inputs": [],
		"name": "pay",
		"outputs": [
			{
				"name": "",
				"type": "uint256"
			}
		],
		"payable": true,
		"stateMutability": "payable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"name": "_name",
				"type": "string"
			},
			{
				"name": "_category",
				"type": "string"
			},
			{
				"name": "_price",
				"type": "uint256"
			},
			{
				"name": "_image",
				"type": "string"
			}
		],
		"payable": false,
		"stateMutability": "nonpayable",
		"type": "constructor"
	}
];
	
	if (typeof window.web3 === 'undefined') {
	    swal(
		  'Ошибка',
		  'Установите MetaMask https://metamask.io, чтобы воспользоваться сервисом.',
		  'warning'
		);
	}
	if (typeof web3 !== 'undefined') {
        web3 = new Web3(web3.currentProvider);
    } else {
        web3 = new Web3(new Web3.providers.HttpProvider("http://localhost:8545"));
    }

    web3.eth.defaultAccount = web3.eth.coinbase;
    $('.rightblock .merchant').attr('href', $('.rightblock .merchant').attr('href')+'/'+ web3.eth.defaultAccount);
    $('.rightblock .customer').attr('href', $('.rightblock .customer').attr('href')+'/'+ web3.eth.defaultAccount);
    if($('.preview').length){
    	$('input[name="name"]').change(function(){
    		$('.product .product__title').html($(this).val());
    	});
    	$('input[name="image"]').change(function(){
    		$('.product .product__image').attr('src', $(this).val());
    	});
    	$('input[name="price"]').change(function(){
    		$('.product .product__price').html($(this).val()+' WEI');
    	});
    	$('input[name="name"]').change();
    	$('input[name="image"]').change();
    	$('input[name="price"]').change();
    }
	$('.new_product').click(function() {
		var qwer = web3.eth.contract(abi).new({
			data: code,
			arguments: [$('input[name="name"]').val(), $('input[name="category"]').val(), $('input[name="price"]').val(), $('input[name="image"]').val()],
	        from: web3.eth.defaultAccount
	    },function(err, transactionHash){
	    	console.log(transactionHash);
	    	waitForElement(transactionHash.transactionHash);
	    	swal(
			  'Ожидание',
			  'Все почти готово. Не закрывайте пожалуйста эту страницу..',
			  'warning'
			);
	    });
	    return false;
	});
	function waitForElement(transactionHash){
		var qwer = web3.eth.getTransactionReceipt(transactionHash, function(err, result){
			console.log(result);
    		if(result && typeof result.contractAddress !== "undefined"){
		        $.ajax({
					type: "POST",
					url: "/createProduct",	
					data: {
						'contract': result.contractAddress,
						'address': web3.eth.defaultAccount,
						'name': $('input[name="name"]').val(),
						'category': $('input[name="category"]').val(),
						'price': $('input[name="price"]').val(),
						'image': $('input[name="image"]').val()
					},
					success: function(data){
						swal(
						  data,
						  'Товар создан, теперь вы можете увидеть его в личном кабинете',
						  'success'
						);
					}
				});
		    } else{
		        setTimeout(waitForElement, 1000, transactionHash);
		    }
    	});
	};
	/* Функция покупки и записи инфы о покупке к нам в бд */
	$('.buy').click(function(){
		var address = $(this).parent().find('.address').val();
		var price = $(this).parent().find('.price').val();
		var contract = window.web3.eth.contract(abi).at(address);
		web3.eth.defaultAccount = web3.eth.coinbase;
		console.log(price);
		web3.eth.sendTransaction({from:web3.eth.defaultAccount, to:address, value:price*10000000000},
            function (error, result) {
            	console.log(result);
                if (!error) {
                	// успешно, надо добавить в бд
                	$.ajax({
						type: "POST",
						url: "/buy",	
						data: {
							'address': web3.eth.defaultAccount,
							'product_address': address
						},
						success: function(data){
							swal(
							  data,
							  'Товар куплен! Просмотреть купленные товары вы можете в личном кабинете',
							  'success'
							);
						}
					});
                } else {
                    swal(
						  'Ошибка!',
						  error,
						  'error'
					);
                }
            }
        );
	});
	/*  Функция подтверждения получения товара */
	$('.confirm').click(function() {
		var address = $('#address').val();
		var contract = window.web3.eth.contract(abi).at(address);
		web3.eth.defaultAccount = web3.eth.coinbase;
		var options = { from: web3.eth.defaultAccount, gas: '3000000'};
		contract.approveReceived(
            options,
            function (error, result) {
                if (!error) {
					swal(
					  data,
					  'Вы подтвердили получение товара.',
					  'success'
					);
                } else {
                    swal(
						  'Ошибка!',
						  error,
						  'error'
					);
                }
            }
        );
	});
	/*  Функция возврата денег за товар */
	$('.refund').click(function() {
		var address = $('#address').val();
		var order = $(this).closest('.order_id').val();
		var contract = window.web3.eth.contract(abi).at(address);
		web3.eth.defaultAccount = web3.eth.coinbase;
		var options = { from: web3.eth.defaultAccount, gas: '3000000'};
		contract.refund(
			order,
            options,
            function (error, result) {
                if (!error) {
					swal(
					  data,
					  'Вы вернули деньги по заказу №' + order,
					  'success'
					);
                } else {
                    swal(
						  'Ошибка!',
						  error,
						  'error'
					);
                }
            }
        );
	});
	/*  Функция возврата денег за товар */
	$('.refund').click(function() {
		var address = $(this).closest('.address').val();
		var order = $(this).closest('.order_id').val();
		var contract = window.web3.eth.contract(abi).at(address);
		web3.eth.defaultAccount = web3.eth.coinbase;
		var options = { from: web3.eth.defaultAccount, gas: '3000000'};
		contract.refund(
			order,
            options,
            function (error, result) {
                if (!error) {
					swal(
					  data,
					  'Вы вернули деньги по заказу №' + order,
					  'success'
					);
                } else {
                    swal(
						  'Ошибка!',
						  error,
						  'error'
					);
                }
            }
        );
	});
	/*  Функция оплаты налогов за товар */
	$('.refund').click(function() {
		var address = $(this).closest('.address').val();
		var contract = window.web3.eth.contract(abi).at(address);
		web3.eth.defaultAccount = web3.eth.coinbase;
		var options = { from: web3.eth.defaultAccount, gas: '3000000'};
		contract.payNalog(
            options,
            function (error, result) {
                if (!error) {
					swal(
					  data,
					  'Вы оплатили налоги за товар' + address,
					  'success'
					);
                } else {
                    swal(
						  'Ошибка!',
						  error,
						  'error'
					);
                }
            }
        );
	});
	/*  Функция оплаты налогов за товар */
	$('.nalog').click(function() {
		var address = $(this).closest('.address').val();
		var contract = window.web3.eth.contract(abi).at(address);
		web3.eth.defaultAccount = web3.eth.coinbase;
		var options = { from: web3.eth.defaultAccount, gas: '3000000'};
		contract.payNalog(
            options,
            function (error, result) {
                if (!error) {
					swal(
					  data,
					  'Вы оплатили налоги за товар' + address,
					  'success'
					);
                } else {
                    swal(
						  'Ошибка!',
						  error,
						  'error'
					);
                }
            }
        );
	});
	/*  Функция вывода полученных денег за товар */
	$('.withdrawal').click(function() {
		var address = $(this).closest('.address').val();
		var contract = window.web3.eth.contract(abi).at(address);
		web3.eth.defaultAccount = web3.eth.coinbase;
		var options = { from: web3.eth.defaultAccount, gas: '3000000'};
		contract.transferOwnMoney(
            options,
            function (error, result) {
                if (!error) {
					swal(
					  data,
					  'Вы вывели деньги за товар' + address,
					  'success'
					);
                } else {
                    swal(
						  'Ошибка!',
						  error,
						  'error'
					);
                }
            }
        );
	}); 
	
	
	function getPrice(address) {
		var contract = web3.eth.contract(abi).at(address);
		web3.eth.defaultAccount = web3.eth.coinbase;
		var options = { from: web3.eth.defaultAccount, gas: '3000000'};
		
		contract.price.call(
                function (error, result){
                    if(!error){
                        console.log(result);
                    } else {
                        console.log(error);
                    }
                });
	};
	
	function getNumBuys(address) {
		var contract = web3.eth.contract(abi).at(address);
		web3.eth.defaultAccount = web3.eth.coinbase;
		var options = { from: web3.eth.defaultAccount, gas: '3000000'};
		
		contract.getnumBuys.call(
                function (error, result){
                    if(!error){
                        console.log(result);
                    } else {
                        console.log(error);
                    }
                });
	};
	
	function getAmount(address) {
		var contract = web3.eth.contract(abi).at(address);
		web3.eth.defaultAccount = web3.eth.coinbase;
		var options = { from: web3.eth.defaultAccount, gas: '3000000'};
		
		contract.getamount.call(
                function (error, result){
                    if(!error){
                        console.log(result);
                    } else {
                        console.log(error);
                    }
                });
	};
	
	function getamountHolded(address) {
		var contract = web3.eth.contract(abi).at(address);
		web3.eth.defaultAccount = web3.eth.coinbase;
		var options = { from: web3.eth.defaultAccount, gas: '3000000'};
		
		contract.getamountHolded.call(
                function (error, result){
                    if(!error){
                        console.log(result);
                    } else {
                        console.log(error);
                    }
                });
	};
	
	function getNalog(address) {
		var contract = web3.eth.contract(abi).at(address);
		web3.eth.defaultAccount = web3.eth.coinbase;
		var options = { from: web3.eth.defaultAccount, gas: '3000000'};
		
		contract.getnalog.call(
                function (error, result){
                    if(!error){
                        console.log(result.c[0]);
                        return result.c[0];
                    } else {
                        console.log(error);
                    }
                });
	};
	
	var adr = "0x3cd584ebe07b64a41d87b10ae3ff18788bdfef34";
	
	
});
