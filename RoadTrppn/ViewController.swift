//
//  ViewController.swift
//  RoadTrppn
//
//  Created by Kathy Zhang on 10/20/18.
//  Copyright © 2018 KZ. All rights reserved.
//

import UIKit
import Alamofire
//import GoogleMaps
//MSServices.proviceAPIKey("AIzaSyANVwaeB8ocI6XPYA8v5rpccSRS2KAaSR8")

class ViewController: UIViewController, UIPickerViewDataSource, UIPickerViewDelegate{

    var datePicker = UIDatePicker()

    
    @IBOutlet weak var pickViewer: UIPickerView!
    
    @IBOutlet weak var streetAddress: UITextField!
    
    @IBOutlet weak var destinationAddress: UITextField!
    
    @IBOutlet weak var startTime: UITextField!
    
    @IBOutlet weak var restTimeStart: UITextField!
    
    @IBOutlet weak var restTimeEnd: UITextField!
    
    
    let cuisine = ["Italian", "Chinese", "Japanese", "Korean", "Thai", "German", "Fast Food"]
    
    func numberOfComponents(in pickerView: UIPickerView) -> Int {
        return 1
    }
    
    func pickerView(_ pickerView: UIPickerView, titleForRow row: Int, forComponent component: Int) -> String? {
        return cuisine[row]
    }
    func pickerView(_ pickerView: UIPickerView, numberOfRowsInComponent component: Int) -> Int {
        return cuisine.count
    }
    //TODO: CUISSDKLJHFASDLHFALSDN
    func createdPicker() {
        datePicker.datePickerMode = .dateAndTime
        let tollbar = UIToolbar()
        tollbar.sizeToFit()
        
        let doneButton = UIBarButtonItem(barButtonSystemItem: .done, target: self, action: #selector(doneac))
        tollbar.setItems([doneButton], animated: true)
        startTime.inputAccessoryView = tollbar
        startTime.inputView = datePicker
        restTimeStart.inputAccessoryView = tollbar
        restTimeStart.inputView = datePicker
        restTimeEnd.inputAccessoryView = tollbar
        restTimeEnd.inputView = datePicker
    }
    
    @objc func doneac() {
        startTime.text = "\(datePicker.date)"
        restTimeStart.text = "\(datePicker.date)"
        restTimeEnd.text = "\(datePicker.date)"
        self.view.endEditing(true)
    }
    
    override func viewDidLoad() {
        super.viewDidLoad()
        streetAddress.delegate = self
        destinationAddress.delegate = self
        createdPicker()
        // Do any additional setup after loading the view, typically from a nib.
    }
    
    @IBAction func submit(_ sender: Any) {
        
        //print("Calling saveToJSONFile()")
        //saveToJsonFile()
        let trimStartTime = startTime.text?.trimmingCharacters(in: .whitespaces)
        let trimStartInterval = restTimeStart.text?.trimmingCharacters(in: .whitespaces)
        let trimEndInterval = restTimeEnd.text?.trimmingCharacters(in: .whitespaces)
        let parameters: Parameters = [
            "startLocation" : streetAddress.text!,
            "endLocation": destinationAddress.text!,
            "startTime" : trimStartTime!,
            "startInterval" : trimStartInterval!,
            "endInterval": trimEndInterval!
        ]
        print(parameters)
        
        Alamofire.request("http://localhost:5000/restaurants",
                          method: .get,
                          parameters: parameters).responseJSON { response in
            print("Request: \(String(describing: response.request))")   // original url request
            print("Response: \(String(describing: response.response))") // http url response
            print("Result: \(response.result)")                         // response serialization result
            
            if let json = response.result.value {
                print("JSON: \(json)") // serialized json response
            }
            
            if let data = response.data, let utf8Text = String(data: data, encoding: .utf8) {
                print("Data: \(utf8Text)") // original server data as UTF8 string
            }
        }
    }
}

extension ViewController : UITextFieldDelegate {
    func textFieldShouldReturn(_ textField: UITextField) -> Bool {
        textField.resignFirstResponder()
        return true
    }
}
