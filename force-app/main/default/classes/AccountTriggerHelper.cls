/**
 * Purpose 		 : Make the Trigger for Account
 *
 * Author 		 : Shalu
 *
 * CreatedByDate : 18-07-2019
 *
 **/
public class AccountTriggerHelper {
  /**
   * Author       : Shalu
   * Created Date : 18-07-2019
   * Name 		: insertChildRecord
   * ReturnType 	: none
   * Parameter 	: List<Account> newListAccount,Map<Id,List<String>> oldMapAccounts
   * Description 	:
   **/
  public static void insertChildRecord(List<Account> newListAccount, Map<Id, Account> oldMapAccounts) {
    Map<Id, List<String>> mapOfAccount = new Map<Id, list<String>>();
    if (newListAccount.size() > 0) {
      for (Account acc : newListAccount) {
        if (acc.Details__c != null && oldMapAccounts == null) {
          if (!mapOfAccount.containsKey(acc.Id)) {
            mapOfAccount.put(acc.Id, new List<String>());
          }
          mapOfAccount.get(acc.Id).addAll(acc.Details__c.split(','));
        }
      }
      if (mapOfAccount.size() > 0) {
        for (String key : mapOfAccount.keySet()) {
        }
      }
    }
  }

  public static void pupulateContactNameOnAccount(List<Account> accounts, Map<Id, Account> accountOldMap) {
    Map<Id, Account> mapOfAccounts = new Map<Id, Account>();
    for (Account acc : accounts) {
      //on change of description field
      if (
        accountOldMap != null &&
        (accountOldMap.get(acc.Id).Description != acc.Description || String.isBlank(acc.Description))
      ) {
        acc.Description = '';
        mapOfAccounts.put(acc.Id, acc);
      }
    }
    //check set size
    if (!mapOfAccounts.isEmpty() && !mapOfAccounts.keySet().isEmpty()) {
      //get contact list
      List<Contact> listOfContacts = [
        SELECT Id, Name, AccountId
        FROM Contact
        WHERE AccountId != NULL AND AccountId IN :mapOfAccounts.keySet()
      ];

      if (!listOfContacts.isEmpty()) {
        //list of accounts to be updated
        Map<Id, Set<String>> mapOfAccountsIdWithContactNames = new Map<Id, Set<String>>();
        for (Contact cont : listOfContacts) {
          if (mapOfAccounts.containsKey(cont.AccountId)) {
            if (
              mapOfAccountsIdWithContactNames.isEmpty() || !mapOfAccountsIdWithContactNames.containsKey(cont.AccountId)
            )
              mapOfAccountsIdWithContactNames.put(cont.AccountId, new Set<String>());
            mapOfAccountsIdWithContactNames.get(cont.AccountId).add(cont.Name);
          }
        }

        if (!mapOfAccountsIdWithContactNames.isEmpty() && !mapOfAccountsIdWithContactNames.keySet().isEmpty()) {
          for (Id accId : mapOfAccountsIdWithContactNames.keySet()) {
            if (mapOfAccounts.containsKey(accId)) {
              mapOfAccounts.get(accId).Description = String.join(
                new List<String>(mapOfAccountsIdWithContactNames.get(accId)),
                '\n'
              );
              System.debug('Come here');
            }
          }
        }
      }
    }
  }
}
